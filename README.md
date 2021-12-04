# sudoku

Sudoku solver written in python. Uses a mask of possible placement positions for each number to implement the following elimination algorithms on top of a recursive guess method:
- if a row, column, or box only has one possible position for a number, place the number there
- if there are no possible placements for a number in a specific row, the board is invalid 
- if the possible positions for a number in a box are arranged in a line, eliminate possible moves in that row/column
  - ex:
  - ![demonstration of line rule](https://user-images.githubusercontent.com/64862590/144693006-509cc1fc-1b85-40a3-b521-a7a4e2020272.png)
