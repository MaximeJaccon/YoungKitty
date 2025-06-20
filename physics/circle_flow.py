from manim import *
import numpy as np

U = 2.0  # stream speed
R = 1.5  # radius

class Flow(Scene):
    def construct(self):
        def velocity_field(pos):
            x, y = pos[:2]
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)  
            if r <= R + 0.01 or r < 0.001: 
                return np.zeros(3)
            
            V_r = U * (1 - (R**2) / (r**2)) * np.cos(theta)
            V_theta = -U * (1 + (R**2) / (r**2)) * np.sin(theta)
            
            V_x = V_r * np.cos(theta) - V_theta * np.sin(theta)
            V_y = V_r * np.sin(theta) + V_theta * np.cos(theta)
            
            return np.array([V_x, V_y, 0])
        
        circle = Circle(radius=R, color=WHITE, fill_opacity=1)
        circle.set_fill(WHITE, opacity=1).set_z_index(30) 
        self.add(circle)
        
        stream_lines = StreamLines(
            velocity_field,
            stroke_width=2,
            virtual_time=3,
            max_anchors_per_line=30,
            x_range=[-8, 8, 0.3],
            y_range=[-8, 8, 0.3],
            colors=[BLUE_D, TEAL],
        )
        
        self.add(stream_lines.set_z_index(-30))
        stream_lines.start_animation(warm_up=True, flow_speed=1)
