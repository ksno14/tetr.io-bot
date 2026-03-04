from copy import deepcopy
from config import BOARD_ROWS, BOARD_COLUMNS


class TetrisGrid:
    def __init__(self, rows: int = BOARD_ROWS, cols: int = BOARD_COLUMNS):
        self.rows = rows
        self.cols = cols
        self.cells = [[0 for _ in range(cols)] for _ in range(rows)]

    def valid_position(self, piece, row, col):
        for r in range(len(piece)):
            for c in range(len(piece[0])):
                if not piece[r][c]:
                    continue
                gr = row + r
                gc = col + c
                if gc < 0 or gc >= self.cols:
                    return False
                if gr >= self.rows:
                    return False
                if gr >= 0 and self.cells[gr][gc]:
                    return False

        return True

    def place_piece(self, piece, row, col):
        for r in range(len(piece)):
            for c in range(len(piece[0])):
                if piece[r][c]:
                    self.cells[row + r][col + c] = 1

    def drop_height(self, piece, col):
        row = -len(piece)
        while self.valid_position(piece, row + 1, col):
            row += 1
        return row

    def clear_lines(self):
        new_board = [row for row in self.cells if not all(cell == 1 for cell in row)]
        cleared = self.rows - len(new_board)
        while len(new_board) < self.rows:
            new_board.insert(0, [0] * self.cols)
        self.cells = new_board
        return cleared

    @staticmethod
    def rotate(piece):
        return [list(row) for row in zip(*piece[::-1])]

    def game_over(self):
        return any(self.cells[0])

    def print(self):
        print()
        header = "    " + " ".join(f"{c:2}" for c in range(self.cols))
        print(header)
        print("   +" + "+".join("--" for _ in range(self.cols)) + "+")

        for r, row in enumerate(self.cells):
            visual_row = self.rows - 1 - r

            line = f"{visual_row:2} |"
            for cell in row:
                line += ("██" if cell else "  ") + "|"

            print(line)
            print("   +" + "+".join("--" for _ in range(self.cols)) + "+")

        print(header)
        print()
