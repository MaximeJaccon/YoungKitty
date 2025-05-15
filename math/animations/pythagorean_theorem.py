from manim import *

class Pythagoras(Scene):
    def construct(self):
        A = ORIGIN
        B = A + UP * 4
        C = A + LEFT * 3
        tri = Polygon(A, B, C, stroke_color=WHITE, fill_color=BLUE,fill_opacity=0.5).move_to(ORIGIN).scale(0.5)
        self.add(tri)
        
        squares = VGroup(*[Square(1,fill_opacity=0.5,fill_color=RED) for _ in range(25)])
        squares.scale(0.5)
        yel_indices = [0, 2, 4, 10, 12, 14, 20, 22, 24]
        yel_sq = VGroup(*[squares[i] for i in yel_indices])
        yel_sq.set_fill(YELLOW)
        red_indices = [i for i in range(25) if i not in yel_indices]
        red_sq = VGroup(*[squares[i] for i in red_indices])
        squares.arrange_in_grid(5,buff=0)
        
        yel_side = yel_sq.copy().arrange_in_grid(3,buff=0)
        red_side = red_sq.copy().arrange_in_grid(4,buff=0)
        red_side.next_to(tri,RIGHT,buff=0)
        yel_side.next_to(tri,DOWN,buff=0)
        
        squares.next_to(yel_side,UL,buff=0)
        squares.rotate(-37 * DEGREES,about_point=squares.get_corner(DR))

        self.add(yel_side,red_side)
        self.wait()
        self.play(ReplacementTransform(
            yel_side.copy(), yel_sq,
            path_arc=-60*DEGREES, path_arc_centers=DL
            ))
        self.play(ReplacementTransform(
            red_side.copy().set_fill(opacity=0),red_sq,
            lag_ratio=0.1,run_time=2))
        self.wait(1)
