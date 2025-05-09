from manim import *

class semicircleWave(Arc):
    def scw_updater(self, mobj, dt):
        if self.timer.get_value() >= self.start_time:
            self.radius = (self.timer.get_value()-self.start_time) * self.wavespeed
            self.generate_points()            
       
    def __init__(self, start_time = 0, timer=None, radius: float = 0, start_angle=-90*DEGREES, angle=180*DEGREES, wavespeed=1, arc_center=ORIGIN,**kwargs):        
        super().__init__(radius, start_angle, angle, arc_center=arc_center,**kwargs)
        self.wavespeed = wavespeed
        self.start_time = start_time
        self.timer = timer
        self.add_updater(self.scw_updater)

class doubleSlit2(Scene):
    def construct(self):
        sceneTime = ValueTracker(0)

        rightMedium = Rectangle(height=8, width=14, stroke_width=0).set_z_index(-1).set_fill(color=BLACK, opacity=1).next_to([-3,0,0],buff=0,direction=RIGHT)
        slits = [-.6,-1.2,.6,1.2]

        wall = VGroup(
            Line([-3,-4,0],[-3,+4,0],color=WHITE,stroke_width=5).set_z_index(0),
            *[Line([-3.1,y,0],[-2.9,y,0],color=BLACK,stroke_width=6).set_z_index(1) for y in slits]
        )
        # distance between wave-start and slit
        wavespeed = 1
        deltaT = {}
        for slit in slits:
            d = np.linalg.norm(np.array([-3,slit,0])-np.array([-7,0,0]))
            deltaT[slit] = d/wavespeed

        self.add(rightMedium,wall)
        densitysteps = 20

        for i in range(20):
            for j in range(densitysteps):
                dens = (np.sin(j*2*PI/densitysteps)/2+0.5)/len(slits)
                self.add(semicircleWave(start_time = i+j/densitysteps, timer = sceneTime, arc_center=[-7,0,0], wavespeed=wavespeed, color=BLUE, stroke_width=100/densitysteps+1,stroke_opacity=dens).set_z_index(-2))

                for slit in slits:
                    self.add(semicircleWave(start_time = i+j/densitysteps+deltaT[slit], timer = sceneTime, arc_center=[-3,slit,0], wavespeed=wavespeed, color=RED, stroke_width=100/densitysteps+1,stroke_opacity=dens).set_z_index(2))

        self.play(sceneTime.animate.set_value(20),rate_func=linear,run_time=20)
