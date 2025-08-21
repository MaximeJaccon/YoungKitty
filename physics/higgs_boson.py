from manim import *

class feynman(Scene):
    def construct(self):
        MyTexTemplate = TexTemplate()
        MyTexTemplate.add_to_preamble(
            r"\usepackage{tikz}"
            r"\usepackage[compat=1.1.0]{tikz-feynman}"
        )

        feyn = Tex(r"""
\begin{tikzpicture}
  \begin{feynman}
    \tikzfeynmanset{
        every fermion/.style={line width=0.6pt, arrow style={scale=0.25}},
        every anti fermion/.style={line width=0.6pt, arrow style={scale=0.25}},
        every gluon/.style={line width=0.6pt},
        every scalar/.style={line width=0.6pt, dashed},
    }

    % Match LaTeX coordinates exactly
    \vertex at (0, 1) (g1) {\(g\)};
    \vertex at (0,-1) (g2) {\(g\)};
    \vertex at (2, 1) (v1);
    \vertex at (2,-1) (v2);
    \vertex at (3.5, 0) (v3);
    \vertex at (5, 0) (higgs);
    \vertex at (2.5, 0) () {\(t\)};
    \vertex at (4.25, 0.3) () {\(H\)};
    \vertex at (5.3, 0.7) () {\(Z\)};
    \vertex at (5.3, -0.7) () {\(Z\)};

    % Higgs decay
    \vertex at (6, 0.8) (z1);
    \vertex at (6, -0.8) (z2);
    \vertex at (8.5, 1.2) (l1) {\(\ell^-\)};
    \vertex at (8.5, 0.4) (l2) {\(\ell^+\)};
    \vertex at (8.5, -0.4) (l3) {\(\ell^-\)};
    \vertex at (8.5, -1.2) (l4) {\(\ell^+\)};

    \diagram* {
        (g1) -- [gluon] (v1),
        (g2) -- [gluon] (v2),
        (v1) -- [fermion] (v2) -- [fermion] (v3) -- [fermion] (v1),
        (v3) -- [dashed] (higgs),
        
        (higgs) -- [boson] (z1),
        (z1) -- [fermion] (l1),
        (z1) -- [anti fermion] (l2),

        (higgs) -- [boson] (z2),
        (z2) -- [fermion] (l3),
        (z2) -- [anti fermion] (l4),
    };
  \end{feynman}
\end{tikzpicture}
""",
        tex_template=MyTexTemplate,
        ).set_stroke(width=2).scale(0.9)


        equation = Tex(
            r"$gg$",
            r"$\rightarrow H$",
            r"$\rightarrow ZZ$",
            r"$\rightarrow \ell^- \ell^+ \ell^- \ell^+$"
        ).shift(3.5*UP)

        self.play(Write(equation))

        self.play(
            Write(feyn[0][0]),
            Write(feyn[0][1]),
            Create(feyn[0][14]),
            Create(feyn[0][15])
        )
        self.wait()

        self.play(
            Create(feyn[0][16:21]),
            Create(feyn[0][21]),
            Write(feyn[0][2])
        )
        self.wait()

        self.play(
            Create(feyn[0][22]),
            Write(feyn[0][3])
        )
        self.wait()

        self.play(
            Create(feyn[0][23]),
            Create(feyn[0][28]),
            Write(feyn[0][4]),
            Write(feyn[0][5])
        )
        self.wait()

        self.play(
            *[Create(feyn[0][i]) for i in range(24, 33) if i != 28],
            Write(feyn[0][6:14])
        )
        self.wait(3)

        '''

        gluon_components = VGroup(
            feyn[0][0],  # g1 label
            feyn[0][1],  # g2 label
            feyn[0][14], # gluon line 1
            feyn[0][15], # gluon line 2
            equation[0]  # gg equation
        )

        # Create a group of everything that's not a gluon
        non_gluon_components = VGroup(*[
            mob for mob in feyn[0] 
            if mob not in gluon_components
        ])

        # Gray out animation
        self.play(
            non_gluon_components.animate.set_opacity(0.3).set_color(GRAY),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            non_gluon_components.animate.set_opacity(1).set_color(WHITE),  # Or original color
            run_time=1.5
        )

        top_quark_loop = VGroup(
            feyn[0][16],
            feyn[0][17],
            feyn[0][18],
            feyn[0][19],
            feyn[0][20],
            feyn[0][21],
            feyn[0][2]
        )

        non_quark = VGroup(*[
            mob for mob in feyn[0] 
            if mob not in top_quark_loop
        ])

        self.play(
            non_quark.animate.set_opacity(0.3).set_color(GRAY),
            run_time=1.5
        )
        self.wait(1)

        '''
