from math import sqrt

'''
- create mask of possible moves for each number
- if mask for a square is arranged in a straight line
	- update mask in that direction
- if mask for a square only contains one item, place that and update mask
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

	def __init__(self, start: list, sidelen: int = 9):
		self.len = sidelen
		self.sqrtlen = sqrt(self.len)

		# useful for solved()
		self.sum = (self.len * (self.len + 1)) // 2
		self.arr = start

		# 9*9 array for 9 numbers
		self.mask = [[[True] * (self.len * self.len)] * self.len]

		# mask of possible positions for each number
		for y in range(self.nums):
			for x in range(self.nums):
				if self.l[y][x] != 0:
					self.update_mask(x, y, 0)

	def __str__(self) -> str:
		vert = '-' * (self.len + sqrt(self.len) + 1)
		out = ''

		for y in range(self.nums):
			if y % self.sq_sz == 0: out += vert + '\n'

			for x in range(self.nums):
				if x % self.sq_sz == 0: out += '|'

				out += str(self[x, y]) if self[x, y] else ' '

			out += '|\n'

		out += vert

		return out
	
	def __getitem__(self, pos: tuple) -> int:
		return self.arr[pos[1] * self.len + pos[0]]
	
	def __setitem__(self, pos: tuple, val: int):
		if val < 0 or val > self.nums:
			raise ValueError

		i = pos[1] * self.len + pos[0]
		prev = self.arr[i]
		self.arr[i] = val

		self.update_mask(x, y, prev)

	# lol
	def __delitem__(self, pos: tuple): pass
	
	def valid(self) -> bool:
		for i in range(self.nums):
			if nonzero_repeats(self.l[i]) or nonzero_repeats(self.cols[i]) or nonzero_repeats(self.squares[i]):
				return False

		return True
	
	def solved(self) -> bool:
		for i in range(self.nums):
			if sum(self.l[i]) != self.num_sum or sum(self.cols[i]) != self.num_sum or sum(self.squares[i]) != self.num_sum:
				return False

		# passed sums test, check if valid
		return self.valid()

	# horrible performance probably
	def valid_place(self, x: int, y: int, n: int) -> bool:
		return self.l[y][x] == 0 and not (n in self.cols[x] or n in self.l[y] or n in self.squares[self.sq_coord(x, y)[0]])

	def update_mask(self, x: int, y: int, prev: int):
		# update square for n
		def update_square(n):
			start_x = x - x % self.sqrtlen
			start_y = y - y % self.sqrtlen

		# if previous was empty or was just set to empty
		update_cur_sq = prev == Sudoku.EMPTY or self[x, y] == Sudoku.EMPTY

		# if previous wasn't empty, have to update previous number's mask
		if prev != Sudoku.EMPTY:
			# loop through sq, recalc
			for i_x, i_y in self.sq_iter(x, y):
				self.mask[prev][i_y][i_x] = self.valid_place(i_x, i_y, n + 1)

			for i in range(self.nums):
				# loop through col, recalc
				self.mask[prev][i][x] = self.valid_place(x, i, n + 1)
				# loop through row, recalc
				self.mask[prev][y][i] = self.valid_place(i, y, n + 1)

			for n in range(self.nums):
				elif update_cur_sq:
					# re-calc position that num was removed at
					self.mask[n][y][x] = self.valid_place(x, y, n + 1)

		if self.l[y][x] != 0:
			# new number has been placed, set to false in every mask
			for n in range(self.nums):
				self.mask[n][y][x] = False

			n = self.l[y][x] - 1

			# loop through cross around x, y
			for i in range(self.nums):
				self.mask[n][y][i] = False
				self.mask[n][i][x] = False
		
			# set all of current sq to false
			for i_x, i_y in self.sq_iter(x, y):
				self.mask[n][i_y][i_x] = False

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
		[0, 0, 0, 0, 0, 0, 2, 0, 0],
		[0, 8, 0, 0, 0, 7, 0, 9, 0],
		[6, 0, 2, 0, 0, 0, 5, 0, 0],
		[0, 7, 0, 0, 6, 0, 0, 0, 0],
		[0, 0, 0, 9, 0, 1, 0, 0, 0],
		[0, 0, 0, 0, 2, 0, 0, 4, 0],
		[0, 0, 5, 0, 0, 0, 6, 0, 3],
		[0, 9, 0, 4, 0, 0, 0, 7, 0],
		[0, 0, 6, 0, 0, 0, 0, 0, 0],
	])


	print(solve_bad(s))
	print(f'backtracks: {backtracks}')

if __name__ == '__main__':
	main()
