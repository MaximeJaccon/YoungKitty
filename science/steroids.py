from manim import *
from mol2chemfigPy3 import mol2chemfig
import io
import contextlib
import sys

class Molecule(Scene):
    def construct(self):

        steroids = {
            #"Estradiol": {
            #       "smiles": "C[C@]12CC[C@H]3[C@H]([C@@H]1CC[C@@H]2O)CCC4=C3C=CC(=C4)O",
            #       "formula": "C18H24O2"
            #   },

            "Aldosterone": {
                "smiles": "C[C@]12CCC(=O)C=C1CC[C@@H]3[C@@H]2[C@H](C[C@]4([C@H]3CC[C@@H]4C(=O)CO)C=O)O",
                "formula": "C_{21} H_{28} O_5"
            },
            "Cortisol": {
                "smiles": "C[C@]12CCC(=O)C=C1CC[C@@H]3[C@@H]2[C@H](C[C@]4([C@H]3CC[C@@]4(C(=O)CO)O)C)O",
                "formula": "C_{21} H_{30} O_5"
            },
            "Pregnenolone": {
                "smiles": "CC(=O)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CC=C4[C@@]3(CC[C@@H](C4)O)C)C",
                "formula": "C_{21} H_{32} O_2"
            },
            "Testosterone": {
                "smiles": "C[C@]12CC[C@H]3[C@H]([C@@H]1CC[C@@H]2O)CCC4=CC(=O)CC[C@]34C",
                "formula": "C_{19} H_{28} O_2"
            },
            "Progesterone": {
                "smiles": "CC(=O)[C@H]1CC[C@@H]2[C@@]1(CC[C@H]3[C@H]2CCC4=CC(=O)CC[C@]34C)C",
                "formula": "C_{21} H_{30} O_2"
            }
        }

        tex_template = TexTemplate()
        tex_template.compiler = "lualatex"
        tex_template.add_to_preamble(r"\usepackage{chemfig}")

        for name, data in steroids.items():
            smiles = data["smiles"]
            formula = data["formula"]

            # Capture chemfig code
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                mol2chemfig(smiles)
                chemfig_code = buf.getvalue().strip()

            if not chemfig_code:
                print(f"Failed to get chemfig code for {name}.")
                continue

            molecule = Tex(
                rf"\chemfig{{{chemfig_code}}}",
                tex_template=tex_template
            ).set_stroke(width=3)

            molecule.scale(0.8)

            label = Text(
                name,
                font_size=28
            )
            formula_text = MathTex(
                formula,
                font_size=35,
                color=BLUE
            )

            label_and_formula = VGroup(label, formula_text).arrange(RIGHT, buff=0.5)
            label_and_formula.next_to(molecule, DOWN, buff=0.5)

            self.play(FadeIn(molecule), FadeIn(label_and_formula))
            self.wait(3)
            self.play(FadeOut(molecule), FadeOut(label_and_formula))

