'''
- create mask of possible moves for each number - DONE
- if mask for a square only contains one item, place that and update mask - DONE
- if mask for a square is arranged in a straight line
	- update mask in that direction
- treat n numbers sharing n tiles in a square as filled squares
'''

from copy import deepcopy

backtracks = 0

class Sudoku:
	EMPTY = -1

	# start is inputted as 1-indexed sudoku board
	def __init__(self, start: list, sidelen: int = 9):
		self.len = sidelen
		self.boxlen = int(self.len ** 0.5)

		# useful for solved()
		self.sum = (self.len * (self.len + 1)) // 2

		# fix array, sub 1 from each
		for i in range(len(start)):
			start[i] -= 1
		self.arr = start

		# 9*9 array for 9 numbers
		self.mask = [[True for _ in range(self.len * self.len)] for _ in range(self.len)]

		# init mask
		for y in range(self.len):
			for x in range(self.len):
				cur = self[x, y]

				if cur == Sudoku.EMPTY:
					continue

				# set mask in cross false
				for i in range(self.len):
					self.set_mask(cur, i, y, False)
					self.set_mask(cur, x, i, False)

					# square to false in every mask
					self.set_mask(i, x, y, False)

				# set mask in square false
				self.iter_square(x, y, lambda x, y: self.set_mask(cur, x, y, False))

	def __str__(self) -> str:
		out = ''
		vert = '-' * (self.len + self.boxlen + 1)

		for y in range(self.len):
			if y % self.boxlen == 0: out += vert + '\n'

			for x in range(self.len):
				if x % self.boxlen == 0: out += '|'

				out += str(self[x, y] + 1) if self[x, y] != Sudoku.EMPTY else ' '

			out += '|\n'

		out += vert

		return out

	# prints selected mask if given, else print whole mask
	def mask_str(self, i: int = None) -> str:
		out = ''
		vert = '-' * ((self.len * self.len + self.len + 1) if i is None else (self.len + self.boxlen + 1))

		for y in range(self.len):
			if y % self.boxlen == 0: out += vert + '\n'

			for x in range(self.len):
				out += '|' if x % self.boxlen == 0 else ('/' if i is None else '')

				if i is not None:
					if self.get_mask(i, x, y):
						out += '+'
					else:
						out += ' ' if self[x, y] == Sudoku.EMPTY else '='
				else:
					for n in range(self.len):
						out += str(n + 1) if self.get_mask(n, x, y) else ' '

			out += '|\n'

		out += vert

		return out

	def __getitem__(self, pos: tuple) -> int:
		return self.arr[pos[1] * self.len + pos[0]]

	def get_mask(self, n: int, x: int, y: int) -> bool:
		return self.mask[n][y * self.len + x]

	# zero indexed number
	def __setitem__(self, pos: tuple, val: int):
		if val < 0 or val >= self.len:
			raise ValueError

		self.arr[pos[0] + pos[1] * self.len] = val

		self.update_mask(*pos)

	def set_mask(self, n: int, x: int, y: int, val: bool):
		self.mask[n][y * self.len + x] = val

	# lol
	def __delitem__(self, pos: tuple): pass
	
	def valid(self) -> bool:
		count = [0] * self.len

		for i in range(self.len):
			for j in range(self.len):
				c = self[i, j]
				r = self[j, i]

				if c == Sudoku.EMPTY or r == Sudoku.EMPTY:
					return False

				count[c] += 1
				count[r] += 1

		for n in count:
			if n != self.len * 2:
				return False

		def sq_chk(x, y): count[self[x, y]] += 1

		for i in range(self.boxlen):
			for j in range(self.boxlen):
				self.iter_square(i, j, sq_chk)

		for n in count:
			if n != self.len * 3:
				return False

		return True
	
	def solved(self) -> bool:
		s = 0

		for i in range(self.len):
			for j in range(self.len):
				c = self[i, j]
				r = self[j, i]

				if c == Sudoku.EMPTY or r == Sudoku.EMPTY:
					return False

				s += c + r + 2 # convert from 0 to 1 indexed

		if s != self.sum * self.len * 2:
			return False

		def sq_sum(x, y):
			nonlocal s
			s += self[x, y] + 1

		for i in range(self.boxlen):
			for j in range(self.boxlen):
				self.iter_square(i, j, sq_sum)

		if s != self.sum * self.len * 3:
			return False

		# passed sums test, check if valid
		return self.valid()

	# passed normal coordinates, iterate over that square
	# if func returns True, return True
	def iter_square(self, x: int, y: int, func):
		start_x = int(x - x % self.boxlen)

		x, y = start_x, int(y - y % self.boxlen)

		for _ in range(self.len):
			if func(x, y) == True:
				return True

			x += 1

			if x == start_x + self.boxlen:
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

	def update_mask(self, x: int, y: int):
		cur = self[x, y]

		# set square to false in mask
		self.iter_square(x, y, lambda x, y: self.set_mask(cur, x, y, False))

		for i in range(self.len):
			# set rows and cols to false in mask
			self.set_mask(cur, i, y, False)
			self.set_mask(cur, x, i, False)

			# set false in every other mask
			self.set_mask(i, x, y, False)


	# pos and val are a guess
	def solve(self, pos: tuple = None, val: int = None):
		global backtracks

		# deepcopy in order to not have to revert moves
		s = deepcopy(self)

		if pos:
			s[pos] = val

		changed = True
		while changed:
			changed = False

			# look for only one valid placement in mask
			for n in range(s.len):
				# check rows and cols
				r_pos, c_pos = -1, -1

				for j in range(s.len):
					for i in range(s.len):
						# uneccessary optimization
						if not r_pos and not c_pos:
							break

						# cannot have multiple in the same row/col
						# set to None if already set
						if s.get_mask(n, i, j):
							r_pos = i if r_pos == -1 else None

						if s.get_mask(n, j, i):
							c_pos = i if c_pos == -1 else None

					# there was only one possible pos in the row/col, so it must be n
					if r_pos and r_pos != -1:
						s[r_pos, j] = n
						changed = True
					if c_pos and c_pos != -1:
						s[j, c_pos] = n
						changed = True

					# reset pos
					r_pos, c_pos = -1, -1

		if s.solved():
			return s

		print(s)
		print(s.mask_str(0))
		exit()

		for y in range(s.len):
			for x in range(s.len):
				# if square is empty
				if s[x, y] == Sudoku.EMPTY:
					# attempt to place all numbers
					for n in range(s.len):
						# if valid
						if s.get_mask(n, x, y):
							# guess
							tmp = s.solve((x, y), n)

							# if the board was valid, return that board
							if tmp: return tmp

		# if no numbers can be placed here
		backtracks += 1
		return None

def main():
	# s = Sudoku([
	# 	2, 0, 0, 0,
	# 	0, 0, 4, 0,
	# 	4, 0, 1, 0,
	# 	0, 0, 0, 0,
	# ], 4)

	s = Sudoku([
		0, 0, 0, 2, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 6, 0, 4, 0, 3,
		0, 0, 0, 0, 0, 5, 0, 7, 0,
		0, 7, 0, 0, 0, 2, 8, 0, 0,
		5, 1, 0, 0, 0, 4, 9, 0, 0,
		0, 0, 9, 0, 0, 3, 0, 0, 0,
		0, 0, 0, 0, 0, 9, 0, 0, 0,
		0, 0, 2, 0, 0, 0, 0, 9, 8,
		0, 8, 3, 1, 0, 0, 2, 0, 0,

		# 5, 3, 0, 0, 7, 0, 0, 0, 0,
		# 6, 0, 0, 1, 9, 5, 0, 0, 0,
		# 0, 9, 8, 0, 0, 0, 0, 6, 0,
		# 8, 0, 0, 0, 6, 0, 0, 0, 3,
		# 4, 0, 0, 8, 0, 3, 0, 0, 1,
		# 7, 0, 0, 0, 2, 0, 0, 0, 6,
		# 0, 6, 0, 0, 0, 0, 2, 8, 0,
		# 0, 0, 0, 4, 1, 9, 0, 0, 5,
		# 0, 0, 0, 0, 8, 0, 0, 7, 9,

		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
		# 0, 0, 0, 0, 0, 0, 0, 0, 0,
	])


	print(s)
	print(s.solve())
	print(f'backtracks: {backtracks}')

if __name__ == '__main__':
	main()
