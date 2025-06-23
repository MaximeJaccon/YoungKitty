from manim import *
import numpy as np
# manim -pql "C:\Users\maxim\.vscode\math\manim\construction\pentadecagon.py" PentadecagonConstruction

class CloseLabelDot(VGroup):
    def __init__(self, position = ORIGIN, label = 0, label_side = True, label_up = False, dot_color = RED, **kwargs):
        dot = Dot(position).scale(0.5).set_color(dot_color).set_z_index(20)
        if label_up==False:
            if label_side==True:
                super().__init__(dot, MathTex(str(label)).scale(0.5).next_to(dot, 0.2*UL), **kwargs)
            else:
                super().__init__(dot, MathTex(str(label)).scale(0.5).next_to(dot, 0.2*DOWN), **kwargs)
        else:
            super().__init__(dot, MathTex(str(label)).scale(0.5).next_to(dot, 0.2*UP), **kwargs)


class AnimatedCircle(VGroup):
    def __init__(self, radius=1.5, center=ORIGIN, radius_color=BLUE, circle_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.center = center
        self.radius_color = radius_color
        self.circle_color = circle_color
        
        self.circle = Circle(radius=radius, color=circle_color).move_to(center)
        
        end_point = center + RIGHT * radius
        self.radius_line = Line(center, end_point, color=radius_color)
        
        self.add(self.circle, self.radius_line)
    
    def create(self, scene, rotation_angle=2*PI, run_time=1, **kwargs):
        """Animate the creation with radius rotation"""
        scene.play(
            Rotate(self.radius_line, angle=rotation_angle, about_point=self.center),
            Create(self.circle),
            run_time=run_time,
            rate_func=smooth,
            **kwargs
        )


class PentadecagonConstruction(MovingCameraScene):
    def construct(self):
        O = CloseLabelDot(label = "O")
        self.play(FadeIn(O, scale=3))
        self.wait()

        A = CloseLabelDot(position = [1.5, 0, 0], label = "A").set_color(BLUE)
        self.play(FadeIn(A, scale=3))
        self.wait()

        animated_X = AnimatedCircle(
            radius=1.5, 
            center=O[0].get_center(),
            radius_color=WHITE,
            circle_color=BLUE
        )
        animated_X.create(self, rotation_angle=2*PI) 
        self.wait()
        self.play(FadeOut(animated_X.radius_line))


        X = animated_X.circle
        X_label = MathTex(r"X").scale(0.5).move_to([-1, 0.8, 0]).set_color(BLUE)

        self.play(FadeIn(X_label, scale=3))
        self.wait()

        lineB = Line(start=[1.5, 0, 0], end=[-1.5, 0, 0]).set_color(RED)
        self.play(Create(lineB))

        B = CloseLabelDot(position=[-1.5,0,0], label="B")
        self.play(FadeIn(B, scale=3))
        self.wait()

        self.play(FadeOut(lineB))

        animated_AB1= AnimatedCircle(
            radius=3, 
            center=A[0].get_center(),
            radius_color=WHITE,
            circle_color=WHITE
        )
        animated_AB2= AnimatedCircle(
            radius=3, 
            center=B[0].get_center(),
            radius_color=WHITE,
            circle_color=WHITE
        )

        animated_AB1.create(self, rotation_angle=2*PI) 
        self.play(FadeOut(animated_AB1.radius_line))
        self.wait()
        animated_AB2.create(self, rotation_angle=2*PI) 
        self.play(FadeOut(animated_AB2.radius_line))
        self.wait()

        C = CloseLabelDot(position=[0, 2.5980762113533, 0], label="C", label_up=True)
        D = CloseLabelDot(position=[0, -2.5980762113533, 0], label="D", label_up=True)
        self.play(LaggedStart(FadeIn(C, scale=3), FadeIn(D, scale=3), lag_ratio=0.2))
        self.wait()

        animated_OAc= AnimatedCircle(
            radius=1.5, 
            center=A[0].get_center(),
            radius_color=WHITE,
            circle_color=WHITE
        )
        animated_OAc.create(self, rotation_angle=2*PI) 
        self.play(FadeOut(animated_OAc.radius_line))
        self.wait()

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=X.width * 2.2))
        self.wait(2)

        E = CloseLabelDot(position=[0.75, 1.2990381056767, 0], label="E", label_up=True)
        F = CloseLabelDot(position=[0.75, -1.2990381056767, 0], label="F", label_up=True)
        self.play(LaggedStart(FadeIn(E, scale=3), FadeIn(F, scale=3), lag_ratio=0.2))
        self.wait()

        lineEF = Line(start=[0.75, 1.2990381056767, 0], end=[0.75, -1.2990381056767, 0]).set_color(RED)
        self.play(Create(lineEF))
        self.wait()

        G = CloseLabelDot(position=[0.75, 0, 0], label="G", label_up=True)
        self.play(LaggedStart(FadeIn(G, scale=3)))
        self.wait()
        self.play(FadeOut(lineEF))

        lineCD = Line(start=[0, 2.5980762113533, 0], end=[0, -2.5980762113533, 0]).set_color(RED)
        self.play(Create(lineCD))
        self.wait()

        H = CloseLabelDot(position=[0, 1.5, 0], label="H", label_up=True)
        self.play(FadeIn(H, scale=3))
        self.wait()
        self.play(FadeOut(lineCD))

        animated_OGc= AnimatedCircle(
            radius=0.75, 
            center=G[0].get_center(),
            radius_color=WHITE,
            circle_color=WHITE
        )
        animated_OGc.create(self, rotation_angle=2*PI) 
        self.play(FadeOut(animated_OGc.radius_line))
        self.wait()

        lineHG = Line(start=H[0].get_center(), end=G[0].get_center()).set_color(RED)
        self.play(Create(lineHG))
        self.wait()

        J = CloseLabelDot(position = [0.4197754203212, 0.6440012327888, 0], label="J", label_up=True)
        self.play(FadeIn(J, scale=3))
        self.wait()
        self.play(FadeOut(lineHG))

        animated_HJc= AnimatedCircle(
            radius=0.953386224451, 
            center=H[0].get_center(),
            radius_color=WHITE,
            circle_color=WHITE
        )
        animated_HJc.create(self, rotation_angle=2*PI) 
        self.play(FadeOut(animated_HJc.radius_line))
        self.wait()

        I = CloseLabelDot(position = [0.903962025432, 1.1970182356757, 0], label="I", label_up=False, label_side=False)
        self.play(FadeIn(I, scale=3))
        self.wait()

        vertices = VGroup()
        for k in range(59):
            angle = k * 2*PI/60
            new_point = O[0].get_center() + np.array([
                np.cos(angle) * (E[0].get_center()[0] - O[0].get_center()[0]) - 
                np.sin(angle) * (E[0].get_center()[1] - O[0].get_center()[1]),
                np.sin(angle) * (E[0].get_center()[0] - O[0].get_center()[0]) + 
                np.cos(angle) * (E[0].get_center()[1] - O[0].get_center()[1]),
                0
            ])
            vertices.add(Dot(new_point).scale(0.5).set_color(RED).set_z_index(20))
        self.play(
            LaggedStart(
                *[Create(vertex) for vertex in vertices],
                lag_ratio=0.02,
                run_time=4
            )
        )
        self.wait()

        self.play(Restore(self.camera.frame))
        self.wait()

        I_dot = Dot(I[0].get_center(), color=RED).scale(0.5).set_z_index(20)
        objects_to_keep = [
            X, 
            *[vertex for vertex in vertices],
            I_dot
        ]

        all_objects = self.mobjects
        objects_to_fade = [
            obj for obj in all_objects 
            if obj not in objects_to_keep and 
               not any(kept_obj in obj for kept_obj in objects_to_keep)
        ]

        stuff = VGroup(X, *[vertex for vertex in vertices], I_dot)

        self.play(
            *[FadeOut(obj) for obj in objects_to_fade],
            stuff.animate.scale(2),
            run_time=1
        )

        small_dots = VGroup()
        for vertex in [*vertices, I_dot]:
            small_dot = Dot(vertex.get_center(), 
                           color=RED, 
                           radius=0.05).set_z_index(20)
            small_dots.add(small_dot)

        self.play(
            Transform(VGroup(*vertices, I_dot), small_dots),
            run_time=1
        )
        self.wait(2)

        vertex_positions = [vertex.get_center() for vertex in vertices] + [I_dot.get_center()]
        colors = color_gradient([BLUE, YELLOW], 7)
        polygons = [
            (60, colors[0]), (30, colors[1]), (15, colors[2]),
            (12, colors[3]), (6, colors[4]), (5, colors[5]), (4, colors[6]), (3, YELLOW)
        ]


        def animate_domino_polygon(scene, vertex_positions, sides, color):
            step = 60 // sides
            angle_step = 2*PI/sides 
            thickness = 8
            flip_time = 0.25 * (3/sides)

            start_point = vertex_positions[0]
            end_point = vertex_positions[step]
            edge = Line(start_point, end_point,
                       color=color,
                       stroke_width=thickness)
            scene.play(Create(edge), run_time=flip_time)

            center = np.mean(vertex_positions, axis=0)

            for i in range(1, sides):
                new_edge = edge.copy()

                rotation_angle = i * angle_step

                new_edge.rotate(rotation_angle, about_point=center)

                new_edge.save_state()
                new_edge.rotate(PI/6, about_point=new_edge.get_start()) 
                new_edge.set_opacity(0)

                scene.add(new_edge)
                scene.play(
                    Restore(new_edge),
                    run_time=flip_time,
                    rate_func=smooth
                )
                scene.wait(flip_time/2)

            # Close the polygon
            closing_edge = Line(vertex_positions[-step], vertex_positions[0],
                              color=color,
                              stroke_width=thickness)
            scene.play(Create(closing_edge), run_time=flip_time)

            return Polygon(*[vertex_positions[(i*step) % 60] for i in range(sides)],
                         color=color,
                         stroke_width=thickness,
                         fill_opacity=0)
        
        polygon_objects = []
        for sides, color in polygons:
            poly = animate_domino_polygon(self, vertex_positions, sides, color)
            polygon_objects.append(poly)
            self.wait(0.5)

        self.wait(5)



class ThumbnailConstruction(Scene):
    def construct(self):
        O = CloseLabelDot(label = "O")
        self.add(O)

        A = CloseLabelDot(position = [1.5, 0, 0], label = "A").set_color(BLUE)
        self.add(A)

        X = Circle(radius=1.5).set_color(BLUE)
        X_label = MathTex(r"X").scale(0.5).move_to([-1, 0.8, 0]).set_color(BLUE)

        self.add(X)
        self.add(X_label)

        lineB = Line(start=[1.5, 0, 0], end=[-1.5, 0, 0]).set_color(RED)
        self.add(lineB)

        B = CloseLabelDot(position=[-1.5,0,0], label="B")
        self.add(B)

        AB1 = Circle(radius=3).move_to(A[0].get_center()).set_color(WHITE)
        AB2 = Circle(radius=3).move_to(B[0].get_center()).set_color(WHITE)

        self.add(AB1)
        self.add(AB2)

        C = CloseLabelDot(position=[0, 2.5980762113533, 0], label="C", label_up=True)
        D = CloseLabelDot(position=[0, -2.5980762113533, 0], label="D", label_up=True)
        self.add(C)
        self.add(D)

        OAc = Circle(radius=1.5).move_to(A[0].get_center()).set_color(WHITE)
        self.add(OAc)

        E = CloseLabelDot(position=[0.75, 1.2990381056767, 0], label="E", label_up=True)
        F = CloseLabelDot(position=[0.75, -1.2990381056767, 0], label="F", label_up=True)
        self.add(E)
        self.add(F)

        lineEF = Line(start=[0.75, 1.2990381056767, 0], end=[0.75, -1.2990381056767, 0]).set_color(RED)
        self.add(lineEF)

        G = CloseLabelDot(position=[0.75, 0, 0], label="G", label_up=True)
        self.add(G)

        lineCD = Line(start=[0, 2.5980762113533, 0], end=[0, -2.5980762113533, 0]).set_color(RED)
        self.add(lineCD)

        H = CloseLabelDot(position=[0, 1.5, 0], label="H", label_up=True)
        self.add(H)

        OGc = Circle(radius=0.75).move_to(G[0].get_center()).set_color(WHITE)
        self.add(OGc)

        lineHG = Line(start=H[0].get_center(), end=G[0].get_center()).set_color(RED)
        self.add(lineHG)

        J = CloseLabelDot(position = [0.4197754203212, 0.6440012327888, 0], label="J", label_up=True)
        self.add(J)

        HJc = Circle(radius=0.953386224451).move_to(H[0].get_center()).set_color(WHITE)
        self.add(HJc)

        I = CloseLabelDot(position = [0.903962025432, 1.1970182356757, 0], label="I", label_up=False, label_side=False)
        self.add(I)
        self.wait()

        im = self.camera.get_image()
        im.save("pentadecagon_construction.png")

        self.wait()
