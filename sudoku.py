from copy import deepcopy, copy

class Sudoku:
	EMPTY = -1

	# only works for 1 digit per square
	def parse(s: str):
		out = []

		for c in s:
			if c == ' ':
				out.append(Sudoku.EMPTY)
			elif c.isdigit():
				out.append(int(c) - 1)

		return Sudoku(out, int(len(out) ** 0.5))

	# start is 0-indexed 1d list
	def __init__(self, start: list, sidelen: int = 9, mask: list = None):
		self.len = sidelen
		self.boxlen = int(self.len ** 0.5)

		# useful for solved(), sum from 0 to len - 1
		self.sum = (self.len * (self.len - 1)) // 2

		self.arr = start

		# len**2 1d array of bools for len numbers
		self.mask = mask if mask else [[True for _ in range(self.len * self.len)] for _ in range(self.len)]

		# not given mask, init
		if mask is None:
			# loop over every number
			for y in range(self.len):
				for x in range(self.len):
					if self.isempty(x, y):
						continue

					# self.update_mask(x, y)

					cur = self[x, y]

					# in cross centered at x, y, set mask to false
					for i in range(self.len):
						self.set_mask(cur, i, y, False)
						self.set_mask(cur, x, i, False)

						# x, y to false in every mask because occupied
						self.set_mask(i, x, y, False)

					# set mask in square false
					self.iter_square(x, y, lambda x, y: self.set_mask(cur, x, y, False))

	from _mask import mask_str, get_mask, set_mask, update_mask, update_line, mask_line
	from _solve import solve

	def __str__(self) -> str:
		out = ''
		vert = '-' * (self.len + self.boxlen + 1)

		for y in range(self.len):
			if y % self.boxlen == 0: out += vert + '\n'

			for x in range(self.len):
				if x % self.boxlen == 0: out += '|'

				out += ' ' if self.isempty(x, y) else str(self[x, y] + 1)

			out += '|\n'

		return out + vert

	def __getitem__(self, pos: tuple) -> int:
		return self.arr[pos[1] * self.len + pos[0]]

	def isempty(self, x: int, y: int) -> bool:
		return self[x, y] == Sudoku.EMPTY

	# zero indexed number
	def __setitem__(self, pos: tuple, val: int):
		if val < 0 or val >= self.len:
			raise ValueError

		self.arr[pos[0] + pos[1] * self.len] = val

		self.update_mask(*pos)

	# lol
	def __delitem__(self, pos: tuple): pass
	
	def valid(self) -> bool:
		for j in range(self.len):
			in_row = [False] * self.len
			in_col = [False] * self.len

			for i in range(self.len):
				if not self.isempty(i, j):
					# row repeat
					if in_row[self[i, j]]: return False

					in_row[self[i, j]] = True
				if not self.isempty(j, i):
					# col repeat
					if in_col[self[j, i]]: return False

					in_col[self[j, i]] = True

		for y in range(0, self.len, self.boxlen):
			for x in range(0, self.len, self.boxlen):
				in_sq = [False] * self.len

				def sq_chk(_x, _y):
					if not self.isempty(_x, _y):
						# square repeat
						if in_sq[self[_x, _y]]: return True

						in_sq[self[_x, _y]] = True

				if self.iter_square(x, y, sq_chk):
					return False

		return True
	
	# sum all rows, cols, squares and check that
	# they equal the sum from 1 to len
	def solved(self) -> bool:
		for i in range(self.len):
			row_sum = 0
			col_sum = 0

			for j in range(self.len):
				if self.isempty(i, j) or self.isempty(j, i):
					return False

				col_sum += self[j, i]
				row_sum += self[i, j]
			
			if row_sum != self.sum or col_sum != self.sum:
				return False

		# guarenteed no empty squares
		for y in range(0, self.len, self.boxlen):
			for x in range(0, self.len, self.boxlen):
				sq_sum = 0

				def f(_x, _y):
					nonlocal sq_sum
					sq_sum += self[_x, _y]

				self.iter_square(x, y, f)

				if sq_sum != self.sum:
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

	def copy(self):
		return Sudoku(
			copy(self.arr),
			self.len,
			deepcopy(self.mask)
		)
