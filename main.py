import time
from vision import TetrisVision
from ai import TetrisAI
from controller import TetrisController
from grid import TetrisGrid
from config import PIECES, SPAWN_COL, PIECE_DELAY


class TetrisAgent:
    def __init__(self, debug: bool = True):
        self.debug = debug

    def _log(self, msg):
        if self.debug:
            print(msg)

    def _wait_for_game_start(self, vision):
        self._log("Leyendo cola inicial...")

        queue = vision.get_next_queue()

        while not all(p != "?" for p in queue):
            time.sleep(0.5)
            queue = vision.get_next_queue()

        self._log(f"Cola inicial detectada: {queue}")

        while True:
            time.sleep(0.2)
            new_queue = vision.get_next_queue()

            if not all(p != "?" for p in new_queue):
                continue

            if new_queue[-1] != queue[-1]:
                self._log("¡Juego iniciado detectado!")
                return queue

    def play(self):
        try:
            print("\nPrepara el juego. Tienes 3 segundos...")
            time.sleep(3)

            vision = TetrisVision(debug_save=True)
            ai = TetrisAI()
            controller = TetrisController()
            grid = TetrisGrid(debug=self.debug)

            queue = self._wait_for_game_start(vision)

            start_time = time.time()
            MAX_DURATION = 120  # segundos

            queue_index = 0
            move_count = 0
            next_queue = None
            hold_piece = None

            while True:
                if time.time() - start_time > MAX_DURATION:
                    print("Tiempo límite alcanzado (2 minutos). Deteniendo agente...")
                    break

                if queue_index >= len(queue):
                    if next_queue is not None:
                        self._log(f"Usando cola pre-cargada: {next_queue}")
                        queue = next_queue
                        next_queue = None
                    else:
                        self._log("Leyendo nueva cola de piezas...")
                        queue = vision.get_next_queue()

                        while not all(p != "?" for p in queue):
                            self._log("Esperando cola completa...")
                            time.sleep(0.5)
                            queue = vision.get_next_queue()

                        self._log(f"Nueva cola detectada: {queue}")

                    queue_index = 0

                current_piece = queue[queue_index]
                current_shape = PIECES.get(current_piece)

                self._log(
                    f"\n[{move_count}] Pieza actual: {current_piece} | Hold: {hold_piece}"
                )

                if queue_index >= len(queue) - 1 and next_queue is None:
                    self._log(
                        "Última pieza de la ronda — pre-cargando siguiente cola..."
                    )
                    candidate = vision.get_next_queue()

                    while not all(p != "?" for p in candidate):
                        self._log("Esperando cola completa...")
                        time.sleep(0.5)
                        candidate = vision.get_next_queue()

                    next_queue = candidate
                    self._log(f"Cola siguiente pre-cargada: {next_queue}")

                use_hold = False

                if hold_piece is None:
                    next_index = queue_index + 1

                    if next_index < len(queue):
                        next_piece = queue[next_index]
                    elif next_queue is not None and len(next_queue) > 0:
                        next_piece = next_queue[0]
                    else:
                        next_piece = None

                    if next_piece is not None:
                        next_shape = PIECES.get(next_piece)
                        move, use_hold = ai.get_best_move_two(
                            current_shape, next_shape, grid
                        )

                        if use_hold:
                            self._log(
                                f"    → Hold vacío: holdeando {current_piece}, jugando {next_piece}"
                            )
                            controller.hold_piece()
                            hold_piece = current_piece
                            queue_index += 1
                            current_piece = next_piece
                            current_shape = next_shape
                    else:
                        move = ai.get_best_move(current_shape, grid)

                else:
                    hold_shape = PIECES.get(hold_piece)
                    move, use_hold = ai.get_best_move_two(
                        current_shape, hold_shape, grid
                    )

                    if use_hold:
                        self._log(
                            f"    → Hold ocupado: holdeando {current_piece}, jugando {hold_piece}"
                        )
                        controller.hold_piece()
                        old_hold = hold_piece
                        hold_piece = current_piece
                        current_piece = old_hold
                        current_shape = hold_shape
                    else:
                        self._log(
                            f"Jugando actual {current_piece}, hold {hold_piece} se conserva"
                        )

                queue_index += 1

                self._log(
                    f"Movimiento: rotaciones={move['rotations']}, col={move['col']}"
                )

                controller.execute_move(
                    move,
                    current_col=SPAWN_COL[current_piece][move["rotations"]],
                )

                drop_row = grid.drop_height(move["piece"], move["col"])
                grid.place_piece(move["piece"], drop_row, move["col"])
                cleared = grid.clear_lines()

                if cleared:
                    self._log(f"    ¡Líneas limpiadas: {cleared}!")

                grid.print()

                if grid.game_over():
                    print("! Game over detectado en grid interno !")
                    break

                move_count += 1

                time.sleep(PIECE_DELAY)

        except KeyboardInterrupt:
            print("\n Bot detenido por el usuario")


if __name__ == "__main__":
    agent = TetrisAgent(debug=True)
    agent.play()
