import time
from copy import deepcopy
from vision import TetrisVision
from ai import TetrisAI
from controller import TetrisController
from grid import TetrisGrid
from config import PIECES, BOARD_COLUMNS, SPAWN_COL, PIECE_DELAY


class TetrisAgent:
    def __init__(self, debug: bool = True):
        self.debug = debug

    def play(self):
        try:
            print("\nPrepara el juego. Tienes 3 segundos...")
            time.sleep(3)

            vision = TetrisVision()
            ai = TetrisAI()
            controller = TetrisController()
            grid = TetrisGrid()

            print("Buscando cola de piezas inicial...")
            queue = vision.get_next_queue()

            while not all(p != "?" for p in queue):
                print("Esperando a que TODAS las piezas sean visibles...")
                time.sleep(0.5)
                queue = vision.get_next_queue()

            print(f"Cola detectada: {queue}. Sincronizando con HOLD...")

            controller.hold_piece()

            queue_index = 0
            move_count = 0
            next_queue = None
            while True:

                if queue_index >= len(queue):
                    if next_queue is not None:
                        print(f"Usando cola pre-cargada: {next_queue}")
                        queue = next_queue
                        next_queue = None
                    else:
                        print("Leyendo nueva cola de piezas...")
                        queue = vision.get_next_queue()

                        while not all(p != "?" for p in queue):
                            print("Esperando cola completa...")
                            time.sleep(0.5)
                            queue = vision.get_next_queue()

                        print(f"Nueva cola detectada: {queue}")

                    queue_index = 0

                current_piece = queue[queue_index]
                queue_index += 1

                shape = PIECES.get(current_piece)

                if self.debug:
                    print(f"\n[{move_count}] Pieza actual: {current_piece}")

                if queue_index >= len(queue) and next_queue is None:
                    print("Última pieza de la ronda — pre-cargando siguiente cola...")
                    candidate = vision.get_next_queue()
                    while not all(p != "?" for p in candidate):
                        print("Esperando cola completa...")
                        time.sleep(0.5)
                        candidate = vision.get_next_queue()
                    next_queue = candidate
                    print(f"Cola siguiente pre-cargada: {next_queue}")

                move = ai.get_best_move(shape, grid)

                if self.debug:
                    print(
                        f"    Movimiento: rotaciones={move['rotations']}, col={move['col']}"
                    )

                controller.execute_move(
                    move, current_col=SPAWN_COL[current_piece][move["rotations"]]
                )

                drop_row = grid.drop_height(move["piece"], move["col"])
                grid.place_piece(move["piece"], drop_row, move["col"])
                cleared = grid.clear_lines()

                if self.debug:
                    if cleared:
                        print(f"    ¡Líneas limpiadas: {cleared}!")
                    grid.print()

                if grid.game_over():
                    print("! Game over detectado en grid interno !")
                    break

                time.sleep(PIECE_DELAY)
                move_count += 1
        except KeyboardInterrupt:
            print("\n Bot detenido por el usuario")


if __name__ == "__main__":
    agent = TetrisAgent(debug=True)
    agent.play()
