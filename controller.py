import time
import pydirectinput
from config import (
    KEY_LEFT,
    KEY_RIGHT,
    KEY_ROTATE,
    KEY_DROP,
    KEY_HOLD,
    KEY_DELAY,
)


class TetrisController:
    def __init__(self):
        pydirectinput.PAUSE = KEY_DELAY

    def move_left(self, times: int):
        for _ in range(times):
            pydirectinput.press(KEY_LEFT)

    def move_right(self, times: int):
        for _ in range(times):
            pydirectinput.press(KEY_RIGHT)

    def rotate(self, times: int):
        for _ in range(times):
            pydirectinput.press(KEY_ROTATE)

    def hard_drop(self):
        pydirectinput.press(KEY_DROP)

    def hold_piece(self):
        pydirectinput.press(KEY_HOLD)

    def execute_move(self, move: dict, current_col: int):
        self.rotate(move["rotations"])

        delta = move["col"] - current_col
        if delta < 0:
            self.move_left(abs(delta))
        elif delta > 0:
            self.move_right(delta)

        self.hard_drop()
