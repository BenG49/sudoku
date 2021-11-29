def arr_init(x: int, y: int, n: int) -> list:
	return [[n for _ in range(x)] for _ in range(y)]

# does not modify original list, l must only contain (1-len(l))
def nonzero_repeats(l: list) -> bool:
	visited = [False] * len(l)

	for n in l:
		if n == 0: continue

		if visited[n - 1]: return True

		visited[n - 1] = True

	return False

class Sudoku:
	# sz = len of smaller square (sqrt of max number)
	def __init__(self, l: list = None, sz: int = 3):
		self.sq_sz = sz if sz > 1 else 3
		# the max number in the game
		self.nums = self.sq_sz * self.sq_sz
		# useful for solved()
		self.num_sum = (self.nums * (self.nums + 1)) // 2

		# if given array is a valid square
		if l and len(l) == self.nums and all(len(r) == self.nums for r in l):
			self.l = l
		else:
			self.l = arr_init(self.nums, self.nums, 0)

		# mirror array arranged in columns
		self.cols = [[self.l[y][x] for y in range(self.nums)] for x in range(self.nums)]

		# mirror array arranged in squares
		self.squares = arr_init(self.nums, self.nums, 0)
		for y in range(self.nums):
			for x in range(self.nums):
				sq, idx = self.sq_coord(x, y)
				self.squares[sq][idx] = self.l[y][x]

		# NOTE: index 0 is number 1
		self.mask = [arr_init(self.nums, self.nums, True) for _ in range(self.nums)]
		# mask of possible positions for each number
		for y in range(self.nums):
			for x in range(self.nums):
				if self.l[y][x] != 0:
					self.update_mask(x, y, 0)
	
	def __getitem__(self, pos: tuple) -> int:
		x, y = pos
		return self.l[y][x]

	def __setitem__(self, pos: tuple, val: int):
		if val < 0 or val > self.nums:
			raise ValueError

		x, y = pos
		prev = self.l[y][x]
		self.l[y][x] = val

		# update mirror arrays
		self.cols[x][y] = val

		i = self.sq_coord(x, y)
		self.squares[i[0]][i[1]] = val

		self.update_mask(x, y, prev)

	# lol
	def __delitem__(self, pos: tuple): pass

	def sq_iter(self, x: int, y: int) -> list:
		s_x = x - (x % self.sq_sz)
		s_y = y - (y % self.sq_sz)
		
		return [(i_x + s_x, i_y + s_y) for i_x in range(self.sq_sz) for i_y in range(self.sq_sz)]

	def sq_coord(self, x: int, y: int) -> tuple:
		return (y // self.sq_sz) * self.sq_sz + x // self.sq_sz, (y % self.sq_sz) * self.sq_sz + x % self.sq_sz
	
	def __str__(self) -> str:
		vert = '-' * (self.nums + self.sq_sz + 1)
		out = ''

		for y in range(self.nums):
			if y % self.sq_sz == 0: out += vert + '\n'

			for x in range(self.nums):
				if x % self.sq_sz == 0: out += '|'

				out += str(self[x, y]) if self[x, y] else ' '

			out += '|\n'

		out += vert

		return out
	
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

	# have to check for every position that could be placed
	# probably shit slow
	def update_mask(self, x: int, y: int, prev: int):
		# because prev was deleted, recalculate all squares
		if prev != 0:
			prev -= 1 # convert from l index to mask index

			# fix up all of the masks
			for n in range(self.nums):
				# only calculate position that's being set for other masks
				if n != prev:
					# re-calc position that num was removed at
					self.mask[n][y][x] = self.valid_place(x, y, n + 1)
				# recalculate row, col, square positions
				else:
					# loop through sq, recalc
					for i_x, i_y in self.sq_iter(x, y):
						self.mask[n][i_y][i_x] = self.valid_place(i_x, i_y, n + 1)

					for i in range(self.nums):
						# loop through col, recalc
						self.mask[n][i][x] = self.valid_place(x, i, n + 1)
						# loop through row, recalc
						self.mask[n][y][i] = self.valid_place(i, y, n + 1)

		# if it wasn't setting to zero
		if self.l[y][x] != 0:
			# new number has been placed, set to false in every mask
			for n in range(self.nums):
				self.mask[n][y][x] = False

			# index
			n = self.l[y][x] - 1

			# loop through cross around x, y, set to false
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

	for n in range(s.nums):
		pass

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

			# reset mask
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
