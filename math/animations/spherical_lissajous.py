from manim import *
import numpy as np

class SphericalLissajous(ThreeDScene):
    def construct(self):
        # Parameters
        m1, m2 = 7, 6
        alpha = 0
        
        sphere = Sphere(radius=1, resolution=(24, 24))
        sphere.set_opacity(0.3)
        sphere.set_color(WHITE)
  
        def lissajous(t):
            x = np.sin(m2*t) * np.cos(m1*t - alpha*np.pi)
            y = np.sin(m2*t) * np.sin(m1*t - alpha*np.pi)
            z = np.cos(m2*t)
            return np.array([x, y, z])
        
        curve = ParametricFunction(
            lissajous,
            t_range=[0, 2*PI, 0.01],
            color=BLUE_B
        )
        
        equation = Tex(
            r"$\ell_\alpha(t) = \big(\sin(m_2 t) \cos(m_1 t - \alpha \pi), "
            r"\sin(m_2 t) \sin(m_1 t - \alpha \pi), \cos(m_2 t)\big),\; t \in \mathbb{R}$"
        ).scale(0.8)

        equation.shift(2*UP)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(Write(equation))

        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES, zoom = 1.2)
        self.begin_ambient_camera_rotation(rate=0.1)
        
        self.play(FadeIn(sphere))
        self.wait(1)
         
        moving_dot = Dot3D(color=BLUE_C, radius=0.03)
        self.add(moving_dot)
        
        curve_tracker = ValueTracker(0)
        moving_dot.add_updater(
            lambda m: m.move_to(
                lissajous(curve_tracker.get_value() * 2*PI)
            )
        )
        
        self.play(
            Create(curve),
            curve_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=15
        )
        moving_dot.clear_updaters()
        self.remove(moving_dot)
        
        self.play(
            FadeOut(equation),
            FadeOut(sphere),
            curve.animate.set_stroke(width=3)
        )
        
        self.play(curve.animate.scale(1.5), run_time=3)
        self.move_camera(phi=75*DEGREES, theta=45*DEGREES, zoom=1.5, run_time=3)

        self.wait(5)
