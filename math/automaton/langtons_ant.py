from manim import *
import numpy as np

class LangtonsAntVid(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        cell_size = 0.1
        steps = 11000

        # Ant state
        pos = np.array([0.0, 0.0, 0.0])
        direction_idx = 0
        grid = {}
        white_squares = VGroup()

        directions = [UP, RIGHT, DOWN, LEFT]

        ant = Square(side_length=cell_size * 0.8)
        ant.set_fill(BLUE, 1).set_stroke(width=0)
        ant.move_to(pos * cell_size)

        self.add(ant, white_squares)

        for step in range(steps):
            current_pos_tuple = tuple(pos[:2])
            cell_color = grid.get(current_pos_tuple, False)  # False = black, True = white

            direction_idx = (direction_idx + (1 if cell_color else -1)) % 4
            grid[current_pos_tuple] = not cell_color

            if not cell_color:
                square = Square(side_length=cell_size)
                square.set_fill(WHITE, 1).set_stroke(width=0)
                square.move_to(pos * cell_size)
                white_squares.add(square)
            else:
                for sq in white_squares:
                    if np.allclose(sq.get_center(), pos * cell_size):
                        white_squares.remove(sq)
                        break

            # Move ant
            pos += directions[direction_idx]
            ant.move_to(pos * cell_size)

            # Render every few steps for performance
            if step % 5 == 0:
                self.remove(white_squares)
                self.add(white_squares, ant)
                self.wait(0.005)

        self.wait()
