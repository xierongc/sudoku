# Solve Sudoku
Use 2 rules and backtracking to solve sudoku issues.
## How to use
For example, use following command line.

sudoku.py -i input.txt -v 0

-i input file which contains sudoku issues.
-v 1 or 0, list verbose solving steps or not.

Format of input file, check input.txt for details.
Start with issue name enclosed by [ ].
Then each line represent those row cells. For empty cell, use 0 to represent it.
Here is the example of one sudoku issue.

[No 92]

0 0 9 0 0 0 0 0 2
 
0 0 0 3 1 0 8 0 0
 
2 0 8 6 0 0 0 0 0

0 5 0 0 2 0 0 0 1
 
0 0 0 4 0 8 0 0 0
 
6 0 0 0 9 0 0 4 0 

0 0 0 0 0 6 4 0 3

0 0 7 0 8 5 0 0 0
 
1 0 0 0 0 0 2 0 0 
 

