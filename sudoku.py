'''
- create mask of possible moves for each number - DONE
- if mask for a square only contains one item, place that and update mask - DONE
- if mask for a square is arranged in a straight line - DONE
- treat n numbers sharing n tiles in a square as filled squares
'''

class Sudoku:
	EMPTY = -1

	# only works for 1 digit per square
	def parse(s: str):
		out = []

		for c in s:
			if not c.isdigit():
				continue

			out.append(int(c) - 1)

		return Sudoku(out, int(len(out) ** 0.5))

	# start is inputted as 0-indexed sudoku board
	def __init__(self, start: list, sidelen: int = 9):
		self.len = sidelen
		self.boxlen = int(self.len ** 0.5)

		# useful for solved()
		self.sum = (self.len * (self.len + 1)) // 2

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

	from _mask import mask_str, get_mask, set_mask, update_mask, update_line, mask_line
	from _solve import solve

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

def main():
	s = Sudoku.parse(
		'''
		001006040
		000000801
		400000000
		500190400
		002800005
		007500600
		000600508
		685709102
		019000000
		'''
		# '''
		# 000200000
		# 000060403
		# 000005070
		# 070002800
		# 510004900
		# 009003000
		# 000009000
		# 002000098
		# 083100200
		# '''
		# '''
		# 002070010
		# 700090020
		# 060040003
		# 090030002
		# 058000100
		# 007000004
		# 900000008
		# 000400200
		# 803001005
		# '''
	)

	print(s)
	print(s.solve())

if __name__ == '__main__':
	main()
