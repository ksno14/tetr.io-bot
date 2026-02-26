import cv2
import numpy as np
import mss
from config import NEXT_REGION, NUM_NEXT_PIECES, PIECE_COLORS


class TetrisVision:
    def __init__(self):
        self.sct = mss.mss()

    def capture_region(self, region: dict) -> np.ndarray:
        raw = self.sct.grab(region)
        img = np.array(raw)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    def _get_mask(self, hsv_img: np.ndarray, piece: str) -> np.ndarray:
        lo, hi = PIECE_COLORS[piece]
        return cv2.inRange(hsv_img, np.array(lo), np.array(hi))

    def detect_piece_in_slot(self, slot_img: np.ndarray) -> str:
        hsv = cv2.cvtColor(slot_img, cv2.COLOR_BGR2HSV)
        best_piece = "?"
        best_count = 50  # Umbral mínimo de píxeles

        for piece in PIECE_COLORS.keys():
            mask = self._get_mask(hsv, piece)
            count = cv2.countNonZero(mask)
            if count > best_count:
                best_count = count
                best_piece = piece
        return best_piece

    def get_next_queue(self) -> list:
        img = self.capture_region(NEXT_REGION)
        h, w = img.shape[:2]
        slot_h = h // NUM_NEXT_PIECES

        pieces = []
        for i in range(NUM_NEXT_PIECES):
            slot = img[i * slot_h : (i + 1) * slot_h, :]
            pieces.append(self.detect_piece_in_slot(slot))

        return pieces
