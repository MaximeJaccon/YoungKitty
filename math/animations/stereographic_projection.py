from manim import *
import numpy as np

class StereographicProjection(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.renderer.camera.light_source.move_to(3*IN + 3*OUT + 5*UP)

        explain = Tex(
            "A ", 
            "stereographic projection", 
            " projects a point on the sphere onto a plane.",
            font_size=36
        )

        explain[1].set_color(BLUE)

        self.add_fixed_in_frame_mobjects(explain)
        self.play(FadeIn(explain))
        self.wait()

        inverse_eq = MathTex(
            r"(x, y, z) = (X, Y) = \Big( \frac{2X}{1 + X^2 + Y^2}, \frac{2Y}{1 + X^2 + Y^2}, \frac{-1 + X^2 + Y^2}{1 + X^2 + Y^2}\Big)",
            font_size=36
        )
        self.add_fixed_in_frame_mobjects(inverse_eq)
        inverse_eq.next_to(explain, DOWN, buff=0.2)
        self.play(FadeIn(inverse_eq))
        self.wait()

        self.play(FadeOut(inverse_eq, explain))
        
        R = 1.5  # Sphere radius

        # Sphere centered at (0,0,R)
        sphere = Sphere(radius=R, resolution=(16, 16))
        sphere.move_to(np.array([0, 0, R]))
        sphere.set_opacity(0.1)
        sphere.set_color(WHITE)
        sphere.set_stroke(WHITE, width=0.5, opacity=0.6)
        self.add(sphere)

        north_pole = Dot3D(point=np.array([0, 0, 2*R]), radius=0.06, color=YELLOW)

        glow_spheres = VGroup()
        num_layers = 5
        for i in range(1, num_layers + 1):
            glow = Sphere(radius=0.08 * i, resolution=(16, 16))
            glow.move_to(np.array([0, 0, 2*R]))
            glow.set_color(YELLOW)
            glow.set_opacity(0.02 * (num_layers + 1 - i))  # decreasing opacity
            glow_spheres.add(glow)
        
        grid = VGroup()

        for angle in np.linspace(0, 2 * np.pi, 20, endpoint=False):
            line = Line(
                start=ORIGIN,
                end=20 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=BLUE_B,
                stroke_opacity=0.5
            )
            grid.add(line)

        num_circles = 8
        for t in np.linspace(0.1, 0.9, num_circles):
            z = R * (1 - 2*t)
            if z != R:
                radius = (2*R * np.sqrt(R**2 - z**2)) / (R - z)
                circle = Circle(
                    radius=radius,
                    color=BLUE,
                    stroke_opacity=0.5
                )
                grid.add(circle)

        self.play(FadeIn(sphere), FadeIn(north_pole), FadeIn(grid))
        self.wait()
        self.play(FadeIn(glow_spheres))
        self.wait()

        x_tracker = ValueTracker(1.5)
        y_tracker = ValueTracker(1.0)

        def get_plane_point():
            return np.array([x_tracker.get_value(), y_tracker.get_value(), 0])

        def get_sphere_point():
            x, y = x_tracker.get_value(), y_tracker.get_value()
            denom = x**2 + y**2 + 4*R**2
            return np.array([
                4 * R**2 * x / denom,
                4 * R**2 * y / denom,
                2 * R * (x**2 + y**2)  / denom 
            ])

        dot_plane = always_redraw(lambda: Dot3D(
            point=get_plane_point(),
            radius=0.05,
            color=RED
        ))

        dot_sphere = always_redraw(lambda: Dot3D(
            point=get_sphere_point(),
            radius=0.05,
            color=RED
        ))

        projection_line = always_redraw(lambda: DashedLine(
            start=north_pole.get_center(),
            end=get_plane_point(),
            color=WHITE,
            stroke_opacity=0.9
        ))

        self.add(projection_line, dot_plane, dot_sphere)
        
        self.play(
            x_tracker.animate.set_value(3.0),
            y_tracker.animate.set_value(2.0),
            run_time=3
        )
        self.play(
            x_tracker.animate.set_value(-2.0),
            y_tracker.animate.set_value(1.5),
            run_time=3
        )
        self.play(
            x_tracker.animate.set_value(0.5),
            y_tracker.animate.set_value(-1.0),
            run_time=3
        )
        self.wait()
