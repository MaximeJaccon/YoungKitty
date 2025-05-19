from manim import *
import numpy as np

class ElectricFieldAnimation(Scene):
    def construct(self):
        pCharge = VGroup(
            Dot(point=[-4, -2, 0], color=RED),
            Dot(point=[0, 1, 0], color=RED),
            Dot(point=[3, -1, 0], color=RED)
        )

        nCharge = VGroup(
            Dot(point=[-2, 2, 0], color=BLUE),
            Dot(point=[2, 2, 0], color=BLUE),
            Dot(point=[5, -2, 0], color=BLUE)
        )

        self.play(Create(pCharge), Create(nCharge))

        def func(pos):
            pds = [pos - p.get_center() for p in pCharge]
            nds = [pos - n.get_center() for n in nCharge]
            pdnorm = [np.linalg.norm(p)+1e-4 for p in pds]
            ndnorm = [np.linalg.norm(n)+1e-4 for n in nds]
            localField = np.array([0.0, 0.0, 0.0])
            if min(pdnorm) >= 0.2 and min(ndnorm) >= 0.2:
                for p, norm in zip(pds, pdnorm):
                    localField += p / norm**3
                for n, norm in zip(nds, ndnorm):
                    localField -= n / norm**3
            return localField

      vf = StreamLines(
            func,
            x_range=[-7, 7, 0.2],
            y_range=[-4, 4, 0.2],
            stroke_width=0.5,
            max_anchors_per_line=400,
            virtual_time=12,
            dt=0.05,
            n_repeats=2,
            padding=1,
        )
        self.add(vf)

        vf.start_animation()
        self.wait(4.0)

        
