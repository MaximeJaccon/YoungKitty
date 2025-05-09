from manim import *
import numpy as np
from scipy.integrate import solve_ivp

def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

def compute_lorenz_trajectory(initial_point, t_max, dt=0.01):
    t_values = np.arange(0, t_max, dt)
    sol = solve_ivp(lorenz_system, (0, t_max), initial_point, t_eval=t_values, method="RK45")
    return sol.y.T  # shape: (n_steps, 3)

class LorenzScatterPoints_nospin(ThreeDScene):
    def construct(self):

        self.set_camera_orientation(phi=70 * DEGREES, theta=135 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.01)
        self.move_camera(frame_center=ORIGIN + 2 * UP)

        axes = ThreeDAxes(
            x_range=(-50, 50, 10),
            y_range=(-50, 50, 10),
            z_range=(0, 60, 10),
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={
                "stroke_width": 1,    
                "include_tip": False, 
                "include_ticks": False
            }
        )
        self.add(axes)

        eq1 = MathTex(r"\frac{dx}{dt} = \sigma(y - x)", font_size=36)
        eq2 = MathTex(r"\frac{dy}{dt} = x(\rho - z) - y", font_size=36)
        eq3 = MathTex(r"\frac{dz}{dt} = x y - \beta z", font_size=36)
      
        equations = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        equations.to_corner(UL)
        equations.shift(2*UP)
        self.add_fixed_in_frame_mobjects(equations)
        
        n_particles = 1000
        t_max = 60
        dt = 0.01

        np.random.seed(0)
        initial_points = np.random.uniform(low=[-20, -20, 0], high=[20, 20, 40], size=(n_particles, 3))

        trajectories = [compute_lorenz_trajectory(p, t_max, dt) for p in initial_points]

        dots = VGroup()
        trails = VGroup()
        trackers = []

        for traj in trajectories:
            dot = Dot3D(radius=0.005, color=WHITE)
            dot.move_to(axes.c2p(*traj[0]))
            dots.add(dot)

            trail = TracedPath(dot.get_center, dissipating_time=0.5, stroke_color=ORANGE, stroke_opacity=[1, 0], stroke_width=0.5)
            trails.add(trail)
            self.add(trail)

            tracker = ValueTracker(0)
            trackers.append((tracker, traj))

        self.play(Create((dots)), Write(equations))

        def update_particles(mob, dt):
            for dot, (tracker, traj) in zip(dots, trackers):
                i = int(tracker.get_value())
                if i < len(traj):
                    dot.move_to(axes.c2p(*traj[i]))
                    tracker.increment_value(0.25)

        dots.add_updater(update_particles)
        self.wait(30)
