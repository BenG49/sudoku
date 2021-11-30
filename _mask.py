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
					out += '•'
				elif self.isempty(x, y):
					out += ' '
				elif self[x, y] == i:
					out += '*'
				else:
					out += '='
			else:
				for n in range(self.len):
					out += str(n + 1) if self.get_mask(n, x, y) else ' '

		out += '|\n'

	out += vert

	return out

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

def update_line(self, x: int, y: int, n: int, pos: tuple):
	# loop from 0 to x, then from x + boxlen to len
	if pos[0] == 0:
		for i in range(0, x):
			self.set_mask(n, i, pos[1], False)

		for i in range(x + self.boxlen, self.len):
			self.set_mask(n, i, pos[1], False)
	# loop from 0 to y, then from y + boxlen to len
	else:
		for i in range(0, y):
			self.set_mask(n, pos[0], i, False)

		for i in range(y + self.boxlen, self.len):
			self.set_mask(n, pos[0], i, False)

# if it finds a line, returns (0, n) for row and (n, 0) for col
def mask_line(self, x: int, y: int, n: int):
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

	if xpos_found != -1 and xpos_found is not None:
		return (xpos_found, 0)
	if ypos_found != -1 and ypos_found is not None:
		return (0, ypos_found)