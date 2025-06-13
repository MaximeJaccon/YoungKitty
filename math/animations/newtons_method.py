class ComplexNewtonsMethod(Scene):
    def construct(self):
        # Create complex plane
        plane = ComplexPlane(
            x_range=(-7, 7),
            y_range=(-7, 7),
            background_line_style={
                "stroke_color": GREY_A,
                "stroke_width": 1,
            }
        )

        original_positions = []
        for x in np.linspace(-7, 7, 50):
            for y in np.linspace(-7, 7, 50):
                original_positions.append(plane.c2p(x, y))
        dots = VGroup(*[
            Dot(plane.c2p(x, y), radius=0.02, color=WHITE)
            for x in np.linspace(-7, 7, 50)
            for y in np.linspace(-7, 7, 50)
        ])
        
        roots = [complex(1, 0), complex(-0.5, 0.866), complex(-0.5, -0.866)]
        colors = [RED, GREEN, BLUE]
        root_dots = VGroup(*[
            Dot(plane.c2p(root.real, root.imag), color=color, radius=0.1)
            for root, color in zip(roots, colors)
        ])
        
        self.add(plane, root_dots, dots)
        self.wait()
        
        for _ in range(10):
            new_dots = VGroup()
            for dot in dots:
                z = complex(*plane.p2c(dot.get_center()))
                
                # Newton step (for z^3 - 1 = 0)
                if abs(z) > 0:
                    new_z = z - (z**3 - 1)/(3*z**2)
                    new_dot = Dot(plane.c2p(new_z.real, new_z.imag), 
                                 color=dot.get_color(), 
                                 radius=dot.radius)
                    new_dots.add(new_dot)
            
            self.play(
                Transform(dots, new_dots),
                run_time=1
            )
            self.wait(0.5)
        
        for dot in dots:
            z = complex(*plane.p2c(dot.get_center()))
            distances = [abs(z - root) for root in roots]
            closest = np.argmin(distances)
            dot.set_color(colors[closest])
        
        self.play(
            dots.animate.set_opacity(0.8),
            run_time=2
        )
        self.wait()

        original_dots = VGroup(*[
            Dot(pos, radius=0.1, color=dots[i].get_color())
            for i, pos in enumerate(original_positions)
        ])
        
        self.play(
            Transform(dots, original_dots),
            run_time=2
        )
        self.wait()
