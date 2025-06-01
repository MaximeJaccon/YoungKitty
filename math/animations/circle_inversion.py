from manim import *
import numpy as np

class CircleInversionTransform(Scene):
    def construct(self):
        circle = Circle(radius=1, color=YELLOW)
        self.add(circle)

        polar_grid = PolarPlane(
            radius_max=50,
            size=100,
            stroke_opacity=1,
            stroke_color=BLUE,
            background_line_style={"stroke_opacity": 0.4},
        )
        self.add(polar_grid)

        def invert(point):
            x, y, z = point
            r_squared = x**2 + y**2
            if r_squared == 0:
                return point
            factor = 1 / r_squared
            return np.array([x * factor, y * factor, z])

        self.play(
            ApplyPointwiseFunction(invert, polar_grid.copy()),
            polar_grid.animate.set_color(GREY),
            run_time=5,
            rate_func=smooth
        )

        self.wait()
