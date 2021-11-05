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
				sq, idx = self.sq_idx(x, y)
				self.squares[sq][idx] = self.l[y][x]

		# NOTE: index 0 is number 1
		self.mask = [arr_init(self.nums, self.nums, True) for _ in range(self.nums)]
		# mask of possible positions for each number
		for y in range(self.nums):
			for x in range(self.nums):
				if self.l[y][x] != 0:
					self.update_mask(x, y)

	# horrible performance probably
	def valid_place(self, x: int, y: int, n: int) -> bool:
		return not (n in self.cols[x] or n in self.l[y] or n in self.squares[self.sq_idx(x, y)[0]])

	def update_mask(self, x: int, y: int, prev: int = None):
		# more complicated
		if self.l[y][x] == 0:
			for n in range(self.nums):
				if n != prev:
					# only set if number is blocking
					self.mask[n][y][x] = self.valid_place(x, y, n)
				else:
					for i in range(self.nums):
						# loop through row
						if self.mask[n][i][x] == 0:
							self.mask[n][i][x] = self.valid_place(x, y, n)
						# loop through col
						if self.mask[y][i][n] == 0:
							self.mask[y][i][n] = self.valid_place(x, y, n)

			return

		# new number has been placed, cannot be placed anywhere else
		for n in range(self.nums):
			self.mask[n][y][x] = False

		n = self.l[y][x] - 1

		# loop through cross around x, y
		for i in range(self.nums):
			self.mask[n][y][i] = False
			self.mask[n][i][x] = False
		
		# set all of current sq to false
		c_x = x - (x % self.sq_sz)
		c_y = y - (y % self.sq_sz)
		for i_y in range(self.sq_sz):
			for i_x in range(self.sq_sz):
				self.mask[n][i_y + c_y][i_x + c_x] = False
	
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

		i = self.sq_idx(x, y)
		self.squares[i[0]][i[1]] = val

		if val == 0:
			self.update_mask(x, y, prev)
		else:
			self.update_mask(x, y)
	
	# lol
	def __delitem__(self, pos: tuple): pass

	def sq_idx(self, x: int, y: int) -> tuple:
		return (y // self.sq_sz) * self.sq_sz + x // self.sq_sz, (y % self.sq_sz) * self.sq_sz + x % self.sq_sz
	
	def __str__(self) -> str:
		vert = '-' * (self.nums + self.sq_sz + 1) + '\n'
		out = ''

		for y in range(self.nums):
			if y % self.sq_sz == 0: out += vert

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

backtracks = 0

# given a valid board, returns None if not solvable
# insanely bad
def solve_bad(s: Sudoku) -> Sudoku:
	global backtracks

	if s.solved():
		return s

	# find first zero
	y = 0
	x = 0
	for y_ in range(s.nums):
		for x_ in range(s.nums):
			if s.l[y_][x_] == 0:
				x, y = x_, y_
				break
		else: continue

	# attempt to place all numbers
	for n in range(1, s.nums + 1):
		# if s.mask[n - 1][y][x]:
		# set and recurse
		s[x, y] = n

		if s.valid():
			# recurse
			tmp = solve_bad(s)

			# if the board was valid, return that board
			if tmp:
				return tmp

	# this board wasn't valid, reset to zero
	s[x, y] = 0
	# if no numbers can be placed here
	backtracks += 1
	return None

def main():
	s = Sudoku([
		[2, 0, 0, 0],
		[0, 0, 4, 0],
		[4, 0, 1, 0],
		[0, 0, 0, 0],
	], 2)

	s = Sudoku([
		[2, 0, 3, 0],
		[0, 0, 4, 0],
		[4, 0, 0, 1],
		[0, 0, 0, 0],
	], 2)

	# s = Sudoku([
	# 	[0, 0, 0, 0, 0, 0, 2, 0, 0],
	# 	[0, 8, 0, 0, 0, 7, 0, 9, 0],
	# 	[6, 0, 2, 0, 0, 0, 5, 0, 0],
	# 	[0, 7, 0, 0, 6, 0, 0, 0, 0],
	# 	[0, 0, 0, 9, 0, 1, 0, 0, 0],
	# 	[0, 0, 0, 0, 2, 0, 0, 4, 0],
	# 	[0, 0, 5, 0, 0, 0, 6, 0, 3],
	# 	[0, 9, 0, 4, 0, 0, 0, 7, 0],
	# 	[0, 0, 6, 0, 0, 0, 0, 0, 0],
	# ])

	print(s.mask[0])
	print(s.mask[2])
	s[2, 0] = 0
	print(s)
	print(s.mask[0])
	print(s.mask[2])

	# print(solve_bad(s))
	# print(f'backtracks: {backtracks}')

if __name__ == '__main__':
	main()
