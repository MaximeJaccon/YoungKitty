import numpy as np
import random
from manim import *

class BlackHoleLightDeflection(Scene):
    def construct(self):
        self.elapsed_time = 0

        def update_time(dt):
            self.elapsed_time += dt

        self.add_updater(update_time)

        black_hole_radius = 0.7
        n_stars = 300

        stars = VGroup(*[
            Dot(
                point=[random.uniform(-7, 7), random.uniform(-4, 4), 0],
                radius=0.05,
                color=WHITE,
                fill_opacity=0.8
            )
            for _ in range(n_stars)
        ])

        plane = NumberPlane( x_range=[-10, 10, 0.5], y_range=[-6, 6, 0.5]).set_opacity(0.3)

        black_hole = Circle(
            radius=black_hole_radius,
            fill_opacity=1
        ).set_color(BLACK)

        event_horizon = Circle(
            radius=black_hole_radius * 1.3,
            stroke_width=2
        ).set_color(BLACK).set_opacity(0.4)

        # Gravitational lensing function
        def lensing_function(p):
            x, y, z = p
            r = np.sqrt(x**2 + y**2)
            if r == 0:
                return p

            deflection_strength = 2.0
            angle_deflection = deflection_strength * np.exp(-r**2)
            theta = np.arctan2(y, x)
            theta_new = theta + angle_deflection
            r_new = r

            x_new = r_new * np.cos(theta_new)
            y_new = r_new * np.sin(theta_new)

            return np.array([x_new, y_new, z])

        plane.prepare_for_nonlinear_transform()

        self.play(FadeIn(stars, shift=IN), Create(plane), run_time=2)
        self.wait(1)

        self.play(
            FadeIn(black_hole, scale=0.5),
            FadeIn(event_horizon, scale=0.5),
            run_time=2
        )
        self.wait(1)

        self.play(
            plane.animate.apply_function(lensing_function),
            run_time=4,
            rate_func=smooth
        )
        self.wait(3)
        self.remove_updater(update_time)
