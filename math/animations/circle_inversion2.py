from manim import *
import numpy as np

class CircleInversionScene(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=False,
            include_foreground_plane=True, 
            foreground_plane_kwargs={
                "x_range": [-7, 7, 0.25],  
                "y_range": [-7, 7, 0.25],  
                "stroke_width": 1.5,
            },
            **kwargs
        )
    
    def construct(self):
        unit_circle = Circle(radius=1, color=YELLOW)
        self.add(unit_circle)
        self.wait(0.5)
        
        # circle inversion function
        def invert_point(point):
            x, y = point[:2]
            r_squared = x**2 + y**2
            if r_squared < 0.001:
                return ORIGIN  
            scale = 2.0  
            return np.array([
                scale * x / r_squared,
                scale * y / r_squared,
                0
            ])

        square = Square(side_length=1.5, color=RED, fill_opacity=0.5)
        square.move_to(np.array([1.5, 1.5, 0]))
        self.add(square)

        square.animate.apply_function(invert_point)
        self.apply_nonlinear_transformation(invert_point)
        self.wait()

        text = Tex("Inversion in a ", "circle").to_corner(UL)
        backgroundrectangle_tex = BackgroundRectangle(text, color=BLACK, fill_opacity=0.5, buff=0.4)
        text[1].set_color(YELLOW)
        self.play(Create(backgroundrectangle_tex), Write(text))
        self.wait()
