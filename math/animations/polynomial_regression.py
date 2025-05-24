import numpy as np
from manim import *

class PolynomialRegressionScene(Scene):
    def construct(self):
        x_vals = np.linspace(-5.5, 5.5, 7)
        y_vals = ((x_vals/3.5)**5 - 2*(x_vals/3.5)**3 + np.random.uniform(-0.8, 0.8, len(x_vals)))

        points = [Dot(point=[x, y, 0], color=WHITE) for x, y in zip(x_vals, y_vals)]
        points_group = VGroup(*points).scale(0.8)
        self.play(*[FadeIn(dot) for dot in points_group])

        coeffs = np.polyfit(x_vals, y_vals, 3)
        poly_func = np.poly1d(coeffs)
        x_range = np.linspace(-7.5, 7.5, 400)
        
        def get_curve(y_values):
            points = np.column_stack([x_range, y_values, np.zeros_like(x_range)])
            curve = VMobject()
            curve.set_points_smoothly(points)
            return curve.set_color(BLUE)
        
        base_y = poly_func(x_range)
        noise_scale = ValueTracker(0.5)
        time_tracker = ValueTracker(0)
        
        def get_noisy_y():
            t = time_tracker.get_value()
            noise = (np.sin(x_range * 1.5 + t * 2) * 0.3 + 
                     np.sin(x_range * 0.7 + t * 1.3) * 0.2 +
                     np.sin(x_range * 3.0 + t * 0.7) * 0.1)
            return base_y + noise * noise_scale.get_value()
        
        curve = always_redraw(lambda: get_curve(get_noisy_y()))
        self.play(Create(curve), run_time=2)
        
        # Animate the noise smoothly
        self.play(
            time_tracker.animate.set_value(20),  # Animate through noise space
            noise_scale.animate.set_value(0.1),  # Gradually reduce noise
            run_time=10,
            rate_func=linear
        )
        
        final_curve = get_curve(base_y)
        self.play(
            Transform(curve, final_curve),
            run_time=1.5,
            rate_func=ease_in_out_sine
        )
        regression_curve = curve
        
        vertical_lines = []
        green_dots = []
        for dot in points:
            x = dot.get_center()[0]
            y_data = dot.get_center()[1]
            y_curve = poly_func(x)
            line = Line(start=[x, y_data, 0], end=[x, y_curve, 0], color=GREEN)
            vertical_lines.append(line)
            green_dot = Dot(point=[x, y_curve, 0], color=GREEN)
            green_dots.append(green_dot)

        self.play(*[Create(line) for line in vertical_lines], *[FadeIn(dot) for dot in green_dots])

        squares = VGroup()
        animations = []
        for line in vertical_lines:
            length = line.get_length()
            square = Square(side_length=length, fill_opacity=0.6, fill_color=GREEN, color=GREEN)
            square.stretch_to_fit_width(0.001).move_to(line.get_center(), aligned_edge=LEFT)
            self.add(square)
            anim = square.animate.stretch_to_fit_width(length)
            squares.add(square)
            animations.append(anim)

        self.play(*animations, FadeOut(*[lin for lin in vertical_lines]), run_time=2)
        self.wait(7)
