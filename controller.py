import time
import pydirectinput
from config import (
    KEY_HOLD,
)


class TetrisController:
    def __init__(self):
        pydirectinput.PAUSE = 0.01

    def hold_piece(self):
        pydirectinput.press(KEY_HOLD)
        time.sleep(2)
