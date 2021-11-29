from math import sqrt

'''
- create mask of possible moves for each number
- if mask for a square is arranged in a straight line
	- update mask in that direction
- if mask for a square only contains one item, place that and update mask
- treat n numbers sharing n tiles in a square as filled squares
'''

# does not modify original list, l must only contain (1-len(l))
def nonzero_repeats(l: list) -> bool:
	visited = [False] * len(l)

	for n in l:
		if n == 0: continue

		if visited[n - 1]: return True

		visited[n - 1] = True

	return False

class Sudoku:
	EMPTY = -1

	# start is inputted as 1-indexed sudoku board
	def __init__(self, start: list, sidelen: int = 9):
		self.len = sidelen
		self.sqrtlen = sqrt(self.len)

		# useful for solved()
		self.sum = (self.len * (self.len + 1)) // 2

		# fix array, sub 1 from each
		for i in range(len(start)):
			start[i] -= 1
		self.arr = start

		# 9*9 array for 9 numbers
		self.mask = [[True for _ in range(self.len * self.len)] for _ in range(self.len)]

		# mask of possible positions for each number
		for y in range(self.len):
			for x in range(self.len):
				if self[x, y] != Sudoku.EMPTY:
					self.update_mask(x, y, 0)

	def __str__(self) -> str:
		vert = '-' * (self.len + sqrt(self.len) + 1)
		out = ''

		for y in range(self.nums):
			if y % self.sq_sz == 0: out += vert + '\n'

			for x in range(self.nums):
				if x % self.sq_sz == 0: out += '|'

				out += str(self[x, y] + 1) if self[x, y] != Sudoku.EMPTY else ' '

			out += '|\n'

		out += vert

		return out
	
	def __getitem__(self, pos: tuple) -> int:
		return self.arr[pos[1] * self.len + pos[0]]

	def get_mask(self, n: int, x: int, y: int) -> bool:
		return self.mask[n][y * self.len + x]
	
	def __setitem__(self, pos: tuple, val: int):
		if val < 0 or val > self.nums:
			raise ValueError

		prev = self[pos]
		self[pos] = val

		self.update_mask(*pos, prev)

	def set_mask(self, n: int, x: int, y: int, val: bool):
		self.mask[n][y * self.len + x] = val

	# lol
	def __delitem__(self, pos: tuple): pass
	
	def valid(self) -> bool:
		for i in range(self.len):
			if nonzero_repeats(self.l[i]) or nonzero_repeats(self.cols[i]) or nonzero_repeats(self.squares[i]):
				return False

		return True
	
	def solved(self) -> bool:
		for i in range(self.len):
			if sum(self.l[i]) != self.num_sum or sum(self.cols[i]) != self.num_sum or sum(self.squares[i]) != self.num_sum:
				return False

		# passed sums test, check if valid
		return self.valid()

	# passed normal coordinates, iterate over that square
	# if func returns True, return True
	def iter_square(self, x: int, y: int, func):
		start_x = int(x - x % self.sqrtlen)

		x, y = start_x, int(y - y % self.sqrtlen)

		for _ in range(self.len):
			val = func(x, y)
			if val == True: return True

			x += 1

			if x == start_x + self.sqrtlen:
				x = start_x
				y += 1

		return False

	def in_row(self, y: int, n: int) -> bool:
		for i in range(self.len):
			if self[i, y] == n: return False
		return True

	def in_col(self, x: int, n: int) -> bool:
		for i in range(self.len):
			if self[x, i] == n: return False
		return True

	# returns if valid for num n to be placed at x, y
	def valid_pos(self, x: int, y: int, n: int, check_row: bool = True, check_col: bool = True) -> bool:
		if self[x, y] != Sudoku.EMPTY: return False
		if check_row and self.in_row(y, n): return False
		if check_col and self.in_col(x, n): return False
		
		# check square
		if self.iter_square(x, y, lambda _x, _y: self[_x, _y] == n):
			return False
	
		return True

	# assumes: prev != cur, prev not in same row, col, or square
	def update_mask(self, x: int, y: int, prev: int):
		cur = self[x, y]

		# set rows, cols, and square to false in mask
		if cur != Sudoku.EMPTY:
			# set square to false in mask
			self.iter_square(x, y, lambda x, y: self.set_mask(cur, x, y, False))

			# set rows and cols to false in mask
			for i in range(self.len):
				self.set_mask(cur, i, y, False)
				self.set_mask(cur, x, i, False)

		# recalc mask for prev in rows, cols, sq
		# recalc mask at x, y for other numbers if cur == empty
		if prev != Sudoku.EMPTY:
			# recalc mask for prev in rows, cols
			for i in range(self.len):
 				# don't need to check if row is valid, iterating over row
				self.set_mask(prev, i, y,
					self.valid_pos(i, y, prev, False))

 				# don't need to check if col is valid, iterating over col
				self.set_mask(prev, x, i,
					self.valid_pos(x, i, prev, check_col=False))

			# recalc mask for prev in sq
			self.iter_square(x, y,
				lambda x, y: self.set_mask(prev, x, y, self.valid_pos(x, y, prev)))

			if cur == Sudoku.EMPTY:
				for i in range(self.len):
					if i != prev:
						self.set_mask(i, x, y, self.valid_pos(x, y, i))

backtracks = 0

# given a valid board, returns None if not solvable
# insanely bad
def solve_bad(s: Sudoku) -> Sudoku:
	global backtracks

	if s.solved():
		return s

	# find first zero
	x = 0
	y = 0
	for j in range(s.nums):
		for i in range(s.nums):
			if s.l[j][i] == 0:
				x, y = i, j
				break
		else:
			continue
		break

	# attempt to place all numbers
	for n in range(1, s.nums + 1):
		# set and recurse
		if s.mask[n - 1][y][x]:
			s[x, y] = n

			# recurse
			tmp = solve_bad(s)

			# if the board was valid, return that board
			if tmp:
				return tmp
			s[x, y] = 0

	# if no numbers can be placed here
	backtracks += 1
	return None

# normal backtracks:   576828, 138 seconds
# backtracks w/ mask: 1070531, 40 seconds

def main():
	# s = Sudoku([
	# 	[2, 0, 0, 0],
	# 	[0, 0, 4, 0],
	# 	[4, 0, 1, 0],
	# 	[0, 0, 0, 0],
	# ], 2)

	s = Sudoku([
		0, 0, 0, 0, 0, 0, 2, 0, 0,
		0, 8, 0, 0, 0, 7, 0, 9, 0,
		6, 0, 2, 0, 0, 0, 5, 0, 0,
		0, 7, 0, 0, 6, 0, 0, 0, 0,
		0, 0, 0, 9, 0, 1, 0, 0, 0,
		0, 0, 0, 0, 2, 0, 0, 4, 0,
		0, 0, 5, 0, 0, 0, 6, 0, 3,
		0, 9, 0, 4, 0, 0, 0, 7, 0,
		0, 0, 6, 0, 0, 0, 0, 0, 0,
	])


	print(solve_bad(s))
	print(f'backtracks: {backtracks}')

if __name__ == '__main__':
	main()
