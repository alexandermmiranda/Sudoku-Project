import random


class SudokuGenerator:
    def __init__(self, size=9, removed_cells=0):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.removed_cells = removed_cells

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) if num != 0 else '.' for num in row))
            if (self.board.index(row) + 1) % 3 == 0:
                print("")  # Adds a blank line for visual separation of 3x3 blocks

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.size)]

    def valid_in_box(self, box_start_row, box_start_col, num):
        for i in range(3):
            for j in range(3):
                if self.board[box_start_row + i][box_start_col + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % 3, col - col % 3, num))

    def fill_diagonal(self):
        for i in range(0, self.size, 3):  # There are three diagonal boxes
            self.fill_box(i, i)

    def fill_box(self, row, col):
        num = 0
        for i in range(3):
            for j in range(3):
                while True:
                    num = random.randint(1, 9)
                    if self.valid_in_box(row, col, num):
                        self.board[row + i][col + j] = num
                        break

    def fill_remaining(self, i, j):
        if j >= self.size and i < self.size - 1:
            i += 1
            j = 0
        if i >= self.size:
            return True
        if i < 3:
            if j < 3:
                j = 3
        elif i < self.size - 3:
            if j == int(i / 3) * 3:
                j += 3
        else:
            if j == self.size - 3:
                i += 1
                j = 0
                if i >= self.size:
                    return True

        for num in range(1, 10):
            if self.is_valid(i, j, num):
                self.board[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.board[i][j] = 0
        return False

    def remove_cells(self):
        count = self.removed_cells
        while count > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count -= 1

    def generate_sudoku(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        self.remove_cells()

sudoku = SudokuGenerator(removed_cells=50)
sudoku.generate_sudoku()
sudoku.print_board()