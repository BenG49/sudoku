# prints selected mask
def mask_str(self, i: int) -> str:
	out = ''
	vert = '-' * (self.len + self.boxlen + 1)

	for y in range(self.len):
		if y % self.boxlen == 0: out += vert + '\n'

		for x in range(self.len):
			if x % self.boxlen == 0: out += '|'

			# valid mask position
			if self.get_mask(i, x, y):
				out += '•'
			elif self.isempty(x, y):
				out += ' '
			# selected number placeed
			elif self[x, y] == i:
				out += '*'
			# occupied square
			else:
				out += '='

		out += '|\n'

	return out + vert

def get_mask(self, n: int, x: int, y: int) -> bool:
	return self.mask[n][y * self.len + x]

def set_mask(self, n: int, x: int, y: int, val: bool):
	self.mask[n][y * self.len + x] = val

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

# given x and y of box, number, and line pos
# sets mask to false in line outside of box
def update_line(self, box_x: int, box_y: int, n: int, pos: tuple):
	# index to set while looping
	idx = 0 if pos[0] == 0 else 1
	loop_var = box_x if idx == 0 else box_y
	pos = list(pos)

	for i in range(0, loop_var):
		pos[idx] = i
		self.set_mask(n, *pos, False)

	for i in range(loop_var + self.boxlen, self.len):
		pos[idx] = i
		self.set_mask(n, *pos, False)

# looks for line in mask, ex
# | = |
# |== |
# |••=|

# returns (0, n) for row and (n, 0) for col
def mask_line(self, x: int, y: int, n: int):
	# looks for points that have all same xpos or ypos
	xpos_found, ypos_found = -1, -1

	def i(_x, _y):
		nonlocal xpos_found, ypos_found

		if self.get_mask(n, _x, _y):
			if xpos_found == -1: xpos_found = _x
			elif xpos_found != _x: xpos_found = None

			if ypos_found == -1: ypos_found = _y
			elif ypos_found != _y: ypos_found = None

			if xpos_found is None and ypos_found is None:
				return True # break

	# points definitely werent in line
	if self.iter_square(x, y, i):
		return None

	# no points were found
	if xpos_found == -1 and ypos_found == -1:
		return None

	# if none, then was repeated
	if xpos_found is not None:
		return (xpos_found, 0)
	if ypos_found is not None:
		return (0, ypos_found)
