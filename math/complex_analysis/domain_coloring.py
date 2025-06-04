from manim import *
import numpy as np
from scipy.special import gamma

RES_X = 512
RES_Y = 288

def complex_to_rgb(z):
    abs_z = np.abs(z)
    arg_z = np.angle(z)

    hue = (arg_z + np.pi) / (2 * np.pi)
    value = 1.0 - 1.0 / (1 + np.log1p(abs_z))
    saturation = 1.0

    return hsv_to_rgb(hue, saturation, value)

def hsv_to_rgb(h, s, v):
    h = np.asarray(h)
    s = np.asarray(s)
    v = np.asarray(v)

    i = np.floor(h * 6).astype(int) % 6
    f = (h * 6) - np.floor(h * 6)

    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r = np.zeros_like(h)
    g = np.zeros_like(h)
    b = np.zeros_like(h)

    mask = (i == 0)
    r[mask], g[mask], b[mask] = v[mask], t[mask], p[mask]
    mask = (i == 1)
    r[mask], g[mask], b[mask] = q[mask], v[mask], p[mask]
    mask = (i == 2)
    r[mask], g[mask], b[mask] = p[mask], v[mask], t[mask]
    mask = (i == 3)
    r[mask], g[mask], b[mask] = p[mask], q[mask], v[mask]
    mask = (i == 4)
    r[mask], g[mask], b[mask] = t[mask], p[mask], v[mask]
    mask = (i == 5)
    r[mask], g[mask], b[mask] = v[mask], p[mask], q[mask]

    return np.stack([r, g, b], axis=-1)

def evaluate_function(Z):
    with np.errstate(divide='ignore', invalid='ignore'):
        return gamma(Z)

def generate_domain_coloring():
    x = np.linspace(-config.frame_width / 2, config.frame_width / 2, RES_X)
    y = np.linspace(-config.frame_height / 2, config.frame_height / 2, RES_Y)
    X, Y = np.meshgrid(x, y[::-1])
    Z = X + 1j * Y

    FZ = evaluate_function(Z)
    pole_mask = np.abs(FZ) > 1e5

    rgb = complex_to_rgb(FZ)
    rgb = np.clip(rgb * 255, 0, 255).astype(np.uint8)

    rgb[pole_mask] = np.array([255, 255, 255], dtype=np.uint8)

    return rgb

class DomainColoringScene(Scene):
    def construct(self):
        self.wait()
        function = MathTex(r"f(z) = \Gamma(z)").to_corner(UL, buff=0.2)
        background = BackgroundRectangle(function, color=BLACK, fill_opacity=0.8, buff=0.4)
        self.add(background)
        self.play(Write(function))
        self.wait()
        RE = Line([-10,0,0], [10,0,0], stroke_width=2.5, color=GREY).set_z_index(-2)
        IM = Line([0,-10,0], [0,10,0], stroke_width=2.5, color=GREY).set_z_index(-1)
        #self.play(Create(RE), Create(IM))
      
        img_array = generate_domain_coloring()
        image = ImageMobject(img_array)
        image.set_z_index(-30).scale(4)

        self.play(FadeIn(image))
        self.wait(2)
        self.play(FadeOut(image))
