from enum import Enum
from typing import List, Tuple
import unittest

class Color(Enum):
	Red = 1
	Green = 2
	Yellow = 3
	Blue = 4 


columns = [
	[Color.Red, Color.Red, Color.Red],
	[None, None, None],
	[None, None, None],
	[None, None, None],
]

columnv2 = [
	[Color.Red, None, None],
	[Color.Red, None, None],
	[Color.Red, None, None],
	[None, None, None],
]

emptyColumns = [[None for _ in range(3)] for _ in range(4)]

def run_algorithm(columns: List[List[Color]]) -> Tuple[List[Color], int]:
	points = 0
	matched = [[False for _ in range(3)] for _ in range(4)]

	# Mark for removal
	for colIdx, column in enumerate(columns):
		for rowIdx, row in enumerate(column):
			if row is not True:
				visited = [[False for _ in range(3)] for _ in range(4)]
				visited, points = recursive_helper(columns, matched, visited, Color.Red, (colIdx, rowIdx), points)

	# Perform removal
	for colIdx, column in enumerate(columns):
		for rowIdx, row in enumerate(column):
			if matched[colIdx][rowIdx] is True:
				columns[colIdx][rowIdx] = None 
		
	# Move items down
	curCol, curRow = 0, 0
	while True:
		if columns[curCol][curRow] is None:
			columns[curCol][curRow] = columns[curCol][curRow + 1] if (curRow + 1) < 3 else None
			if curRow + 1 < 3:
				columns[curCol][curRow + 1] = None
		curRow += 1
		if curRow > 2:
			curCol += 1
			curRow = 0
		if curCol == len(columns):
			break

	return (columns, points)


def recursive_helper(columns: List[Color], matched: List[bool], visited: List[bool], color: Color, currentPosition: Tuple[int, int], points: int) -> Tuple[List[Color], int]:
	(col, row) = currentPosition
	# Test for out of bounds
	if row < 0 or row > 2:
		return visited, points
	if col < 0 or col >= len(columns):
		return visited, points

	# Have we visited already?
	if visited[col][row] is True:
		return visited, points
	else:
		visited[col][row] = True

	# Is it a match?
	if columns[col][row] != color:
		return visited, points
	else:
		matched[col][row] = True

	# Test with the surrounding four
	visited, points = recursive_helper(columns, matched, visited, color, (col - 1, row), points)
	visited, points = recursive_helper(columns, matched, visited, color, (col + 1, row), points)
	visited, points = recursive_helper(columns, matched, visited, color, (col, row - 1), points)
	visited, points = recursive_helper(columns, matched, visited, color, (col, row + 1), points)
	
	return visited, points

class Tests(unittest.TestCase):
	def test_init(self):
		copiedColumns = emptyColumns.copy()
		self.assertEqual(copiedColumns, emptyColumns)

	def test_clear_column(self):
		copiedColums = columns.copy()
		copiedColums, points = run_algorithm(copiedColums)
		self.assertEqual(copiedColums, emptyColumns)

	def test_clear_row(self):
		copiedColumns = columnv2.copy()
		copiedColumns, points = run_algorithm(copiedColumns)
		self.assertEqual(copiedColumns, emptyColumns)

if __name__ == "__main__":
	unittest.main()