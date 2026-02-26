import time
from vision import TetrisVision
from ai import TetrisAI
from controller import TetrisController
from grid import TetrisGrid


class TetrisAgent:
    def __init__(self, lookahead):
        self.lookahead = lookahead

    def play(self):
        print("\nPrepara el juego. Tienes 3 segundos...")
        time.sleep(3)
        vision = TetrisVision()
        ai = TetrisAI()
        controller = TetrisController()
        grid = TetrisGrid()

        print("Buscando cola de piezas inicial...")
        initial_queue = vision.get_next_queue()

        while not all(p != "?" for p in initial_queue):
            print("Esperando a que TODAS las piezas sean visibles...")
            time.sleep(0.5)
            initial_queue = vision.get_next_queue()

        print(f"Cola detectada: {initial_queue}. Sincronizando con HOLD...")
        current_piece = initial_queue[0]
        controller.hold_piece()


if __name__ == "__main__":
    agent = TetrisAgent(5)
    agent.play()
