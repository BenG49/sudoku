'''
- create mask of possible moves for each number - DONE
- if mask for a square only contains one item, place that and update mask - DONE
- if mask for a square is arranged in a straight line - DONE
- if no possible positions for number in row, invalid board - DONE
- treat n numbers sharing n tiles in a square as filled squares
'''

# global variable used to measure algorithm
backtracks = 0

# given position of a guess
def solve(self, guess_pos: tuple = None, guess_val: int = None):
	global backtracks

	# deepcopy in order to not have to revert moves
	s = self.copy()

	if guess_pos:
		s[guess_pos] = guess_val

	changed = True
	# keep track of mask lines that have been found
	lines = []
	# iterate until no changes are made
	while changed:
		changed = False

		# look for rows or cols with one valid place in row/col
		for n in range(s.len):
			for j in range(s.len):
				row_pos, col_pos = -1, -1

				for i in range(s.len):
					# already found repeats in row and col
					if not row_pos and not col_pos:
						break

					# set to none if n has already been found in row/col
					if s.get_mask(n, i, j):
						row_pos = i if row_pos == -1 else None

					if s.get_mask(n, j, i):
						col_pos = i if col_pos == -1 else None

				# only one possible placement in the row/col, must be n
				if row_pos and row_pos != -1:
					s[row_pos, j] = n
					changed = True
				if col_pos and col_pos != -1:
					s[j, col_pos] = n
					changed = True

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

		# look through every box and check if there is a line
		for y in range(0, s.len, s.boxlen):
			for x in range(0, s.len, s.boxlen):
				# loop through every number
				for n in range(s.len):
					t = s.mask_line(x, y, n)

					# if a line was found and not previously found
					if t is not None and t not in lines:
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
			# check that there is at least one valid position in the row
			for x in range(s.len):
				# possible placement
				if s.isempty(x, y) and s.get_mask(n, x, y):
					# recurse with guess
					tmp = s.solve((x, y), n)

					# if board was valid, return
					if tmp:
						return tmp

				elif s[x, y] == n:
					# if in row, there should be no more valid positions
					break

			# if did not break (n was not found in row)
			else:
				# no possible positions in row, invalid
				backtracks += 1
				return None
