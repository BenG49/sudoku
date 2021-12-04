'''
- create mask of possible moves for each number - DONE
- if mask for a square only contains one item, place that and update mask - DONE
- if mask for a square is arranged in a straight line - DONE
- if no possible positions for number in row, invalid board - DONE
- treat n numbers sharing n tiles in a square as filled squares
'''

backtracks = 0

# given position of a guess
def solve(self, pos: tuple = None, val: int = None):
	global backtracks

	# deepcopy in order to not have to revert moves
	s = self.copy()

	if pos:
		s[pos] = val

	changed = True
	# keep track of mask lines that have been found
	lines = []
	while changed:
		changed = False

		# look for rows or cols where theres only one valid place in row/col
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

		# loop through every square and look for only one valid spot
		for y in range(0, s.len, s.boxlen):
			for x in range(0, s.len, s.boxlen):
				for n in range(s.len):
					found = None

					def f(_x, _y):
						nonlocal found
						if s.get_mask(n, _x, _y):
							if found is not None: return True
							found = (_x, _y)

					if not s.iter_square(x, y, f) and found is not None:
						s[found] = n

		# look through every square and check if there is a line
		# in the mask
		# ex
		# | = |
		# |== |
		# |••=|
		for y in range(0, s.len, s.boxlen):
			for x in range(0, s.len, s.boxlen):
				# loop through every number
				for n in range(s.len):
					t = s.mask_line(x, y, n)

					if t is not None:
						if t not in lines:
							changed = True
							lines.append(t)

						s.update_line(x, y, n, t)

	if s.solved():
		print(f'backtracks: {backtracks}')
		backtracks = 0
		return s

	# loop through every number
	for n in range(s.len):
		# loop through every row
		for y in range(s.len):
			in_row = False

			# check that there is at least one valid position
			for x in range(s.len):
				if s.isempty(x, y) and s.get_mask(n, x, y):
					# recurse with guess
					tmp = s.solve((x, y), n)

					# if board was valid, return
					if tmp:
						return tmp
				elif s[x, y] == n:
					in_row = True

			# no possible positions in row, invalid
			if not in_row:
				backtracks += 1
				return None
