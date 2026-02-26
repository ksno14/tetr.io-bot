from config import BOARD_ROWS, BOARD_COLUMNS


class TetrisGrid:
    def __init__(self, rows: int = BOARD_ROWS, cols: int = BOARD_COLUMNS):
        self.rows = rows
        self.cols = cols
        self.cells = [[0] * cols for _ in range(rows)]
