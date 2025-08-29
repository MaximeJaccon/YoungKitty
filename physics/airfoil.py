from manim import *
import numpy as np
import cmath

U = 2.0  # Stream speed
R = 1.2  # Radius of the circle
CENTER = -0.15 + 0.15j  # Offset center
GAMMA = 0  # Kutta condition

class AirfoilFlow(Scene):
    def construct(self):
        plane = ComplexPlane().set_opacity(0)
        self.add(plane)

        def joukowski(z):
            return z + 1 / z

        def inverse_joukowski(zeta):
            discriminant = zeta**2 - 4
            z1 = (zeta + cmath.sqrt(discriminant)) / 2
            z2 = (zeta - cmath.sqrt(discriminant)) / 2
            return z1 if abs(z1) > 1 else z2

        def velocity_circle(z):
            return -U * (1 - R**2 / z**2) + (1j * GAMMA) / (2 * np.pi * z)

        def airfoil_velocity(pos):
            x, y = pos[:2]
            zeta = complex(-x, -y)
            
            if abs(zeta) < 0.1:
                return np.zeros(3)

            z = inverse_joukowski(zeta)
            z_shifted = z + CENTER

            if abs(z_shifted) <= R + 0.01:
                return np.zeros(3)

            V_z = velocity_circle(z_shifted)
            dz_dzeta = 1 - 1 / z**2
            V_zeta = V_z / dz_dzeta

            return np.array([-V_zeta.real, V_zeta.imag, 0])

        airfoil_points = [
            plane.n2p(complex(joukowski(CENTER + R * np.exp(1j * theta)).real, 
                     joukowski(CENTER + R * np.exp(1j * theta)).imag))
            for theta in np.linspace(0, 2 * np.pi, 200)
        ]
        airfoil = Polygon(*airfoil_points, color=WHITE, fill_opacity=1)

        stream_lines = StreamLines(
            airfoil_velocity,
            stroke_width=2,
            virtual_time=4,
            max_anchors_per_line=30,
            x_range=[-8, 8, 0.3],
            y_range=[-6, 6, 0.3],
            colors=[BLUE_D, TEAL],
        )

        self.play(Create(airfoil))
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1)
        self.wait(10)
        im = self.camera.get_image()
        im.save("airfoil_stream.png")

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()
