from manim import *
import numpy as np
from scipy.spatial.transform import Rotation as R


class HopfFibration(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_focal_distance(5)
        
        num_fibers = 100  
        num_points_per_fiber = 50  
        sphere_radius = 2.5
        fiber_radius = 0.1
        
        # Create the base S² sphere (just the surface)
        base_sphere = Sphere(radius=sphere_radius, resolution=(24, 24))
        base_sphere.set_color(BLUE_E)
        base_sphere.set_opacity(0.3)
        
        # Create the S³ sphere (as wireframe)
        s3_sphere = Sphere(radius=sphere_radius, resolution=(12, 12))
        s3_sphere.set_color(WHITE)
        s3_sphere.set_opacity(0.2)
        
        s3_sphere_wireframe = Surface(
            lambda u, v: np.array([
                sphere_radius * np.cos(u) * np.cos(v),
                sphere_radius * np.cos(u) * np.sin(v),
                sphere_radius * np.sin(u)
            ]),
            u_range=[-PI/2, PI/2],
            v_range=[0, TAU],
            checkerboard_colors=False,
            stroke_color=WHITE,
            stroke_width=1,
            fill_opacity=0
        )
        
        # Hopf map: S³ → S²
        def hopf_map(x, y, z, w):
            """Map from S³ to S² using Hopf fibration"""
            return np.array([
                2*(x*z + y*w),
                2*(y*z - x*w),
                x**2 + y**2 - z**2 - w**2
            ])
        
        fibers = VGroup()
        fiber_lines = VGroup()
        
        theta_values = np.linspace(0, PI, num_fibers)
        phi_values = np.linspace(0, 2*PI, num_fibers, endpoint=False)
        
        for theta, phi in zip(theta_values[1:-1], phi_values[1:-1]):  # Skip poles
            s2_point = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ]) * sphere_radius
            

            fiber_points = []
            for t in np.linspace(0, 2*PI, num_points_per_fiber, endpoint=False):
                # Coordinates in S³ that map to this point in S²
                alpha = theta / 2
                x = np.cos(alpha) * np.cos(phi/2 + t)
                y = np.cos(alpha) * np.sin(phi/2 + t)
                z = np.sin(alpha) * np.cos(-phi/2 + t)
                w = np.sin(alpha) * np.sin(-phi/2 + t)
                
                fiber_point = np.array([x, y, z]) * sphere_radius
                fiber_points.append(fiber_point)
            
            fiber = VMobject()
            fiber.set_points_as_corners([*fiber_points, fiber_points[0]])
            fiber.set_color(interpolate_color(YELLOW, RED, theta/PI))
            fiber.set_stroke(width=2)
            fibers.add(fiber)
            
        self.begin_ambient_camera_rotation(rate=0.2)
        
        self.play(Create(s3_sphere_wireframe), FadeIn(base_sphere), run_time=1)
        self.wait(0.5)
        
        
        self.play(
            LaggedStart(*[Create(fiber) for fiber in fibers]),
            LaggedStart(*[Create(line) for line in fiber_lines]),
            run_time=4
        )
        self.wait(1)
        
        def update_fibers(fibers, dt):
            rot_angle = dt * 0.5  # Rotation speed
            rot_matrix = R.from_euler('z', rot_angle).as_matrix()
            
            for fiber in fibers:
                new_points = []
                points = fiber.get_points()
                for i in range(0, len(points)-3, 3): 
                    point = points[i:i+3]
                    rotated_point = np.dot(rot_matrix, point)
                    new_points.extend(rotated_point)
                new_points.append(new_points[0:3])
                fiber.set_points_as_corners(np.array(new_points))
        
        fibers.add_updater(update_fibers)
        self.wait(8)
        fibers.remove_updater(update_fibers)
        self.wait(2)
