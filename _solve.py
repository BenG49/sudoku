'''
- create mask of possible moves for each number - DONE
- if mask for a square only contains one item, place that and update mask - DONE
- if mask for a square is arranged in a straight line - DONE
- treat n numbers sharing n tiles in a square as filled squares

big optimization:
instead of guessing every single open mask, guess only for a certain
number in an area, and if none of positions work

can operate on row, col, square
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
	for y in range(0, s.len, s.boxlen):
		for x in range(0, s.len, s.boxlen):
			# loop through every number
			for n in range(s.len):
				print(f'testing {n} in square {x}, {y}')
				in_square = False

				# check if there is at least one valid position for each number
				def has_valid(_x, _y):
					if s.isempty(_x, _y) and s.get_mask(n, _x, _y):
						print('recursing')
						# recurse, test if actually valid
						tmp = s.solve((_x, _y), n)
						if tmp:
							return tmp
					elif s[_x, _y] == n:
						print('in square')
						in_square = True

				s.iter_square(x, y, has_valid)

				if not in_square:
					backtracks += 1
					return None

	#for y in range(s.len):
	#	for x in range(s.len):
	#		# if square is empty
	#		if s.isempty(x, y):
	#			# attempt to place all numbers
	#			for n in range(s.len):
	#				# if valid
	#				if s.get_mask(n, x, y):
	#					# guess
	#					tmp = s.solve((x, y), n)

	#					# if the board was valid, return that board
	#					if tmp: return tmp

	# if no numbers can be placed here
	backtracks += 1
	return None
