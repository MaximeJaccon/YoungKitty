from manim import *

class ModularCircle(Scene):
    def construct(self):
        mod_tracker = ValueTracker(0)
        circle = Circle()
        circle.scale(3.5).set_color(WHITE)
        lines = self.get_obj(circle, mod_tracker.get_value())
        lines.add_updater(
            lambda m: m.become(
                self.get_obj(circle, mod_tracker.get_value())
            )
        )
        self.play(Create(circle))
        self.play(Create(lines))
        self.wait()
        self.play(
            mod_tracker.animate.set_value(25),
            rate_func=linear,
            run_time=30
        )
        self.wait(3)

    def get_obj(self, circle, mod):
        lines = VGroup()
        for i in range(200):
            start = circle.point_from_proportion((i%200)/200)
            end = circle.point_from_proportion(((i*mod)%200)/200)
            line = Line(start, end).set_stroke(width=1)
            lines.add(line)
        lines.set_color_by_gradient(*[ORANGE,YELLOW,BLUE])
        return lines
