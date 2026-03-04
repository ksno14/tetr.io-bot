from copy import deepcopy
from grid import TetrisGrid
from config import BOARD_COLUMNS


class TetrisAI:
    def __init__(
        self,
        height_weight: float = 0.510066,
        lines_weight: float = 0.760666,
        holes_weight: float = 0.35663,
        bumpiness_weight: float = 0.184483,
    ):
        self.height_weight = height_weight
        self.lines_weight = lines_weight
        self.holes_weight = holes_weight
        self.bumpiness_weight = bumpiness_weight

    def _aggregate_height(self, grid: TetrisGrid) -> int:
        total = 0
        for c in range(grid.cols):
            for r in range(grid.rows):
                if grid.cells[r][c]:
                    total += grid.rows - r
                    break
        return total

    def _lines(self, grid: TetrisGrid) -> int:
        return sum(1 for row in grid.cells if all(cell for cell in row))

    def _holes(self, grid: TetrisGrid) -> int:
        holes = 0
        for c in range(grid.cols):
            block_found = False
            for r in range(grid.rows):
                if grid.cells[r][c]:
                    block_found = True
                elif block_found:
                    holes += 1
        return holes

    def _bumpiness(self, grid: TetrisGrid) -> int:
        heights = []
        for c in range(grid.cols):
            height = 0
            for r in range(grid.rows):
                if grid.cells[r][c]:
                    height = grid.rows - r
                    break
            heights.append(height)
        return sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))

    def _score(self, grid: TetrisGrid) -> float:
        return (
            -self.height_weight * self._aggregate_height(grid)
            + self.lines_weight * self._lines(grid)
            - self.holes_weight * self._holes(grid)
            - self.bumpiness_weight * self._bumpiness(grid)
        )

    def _best(self, grid: TetrisGrid, piece_shape: list) -> dict:
        best_score = None
        best_move = None

        for rotations in range(4):
            rotated = deepcopy(piece_shape)
            for _ in range(rotations):
                rotated = TetrisGrid.rotate(rotated)

            piece_width = len(rotated[0])

            for col in range(-1, BOARD_COLUMNS - piece_width + 2):
                test_grid = deepcopy(grid)
                drop_row = test_grid.drop_height(rotated, col)

                if not test_grid.valid_position(rotated, drop_row, col):
                    continue

                test_grid.place_piece(rotated, drop_row, col)
                test_grid.clear_lines()

                score = self._score(test_grid)

                if best_score is None or score > best_score:
                    best_score = score
                    best_move = {
                        "rotations": rotations,
                        "col": col,
                        "piece": rotated,
                    }

        return best_move

    def get_best_move(self, piece_shape: list, grid: TetrisGrid) -> dict:
        move = self._best(grid, piece_shape)
        if move is None:
            return {"rotations": 0, "col": 0, "piece": piece_shape}
        return move
