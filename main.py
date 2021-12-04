from sudoku import Sudoku

def main():
	s = Sudoku.parse(
		'''
		-------------
		|   |2  |   |
		|   | 6 |4 3|
		|   |  5| 7 |
		-------------
		| 7 |  2|8  |
		|51 |  4|9  |
		|  9|  3|   |
		-------------
		|   |  9|   |
		|  2|   | 98|
		| 83|1  |2  |
		-------------
		'''
	)

	print(s)
	print(s.solve())

if __name__ == '__main__':
	main()
