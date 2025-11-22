from manim import *

TITLE_COLOR = GREEN_E
SUBTITLE_COLOR = GREY_B
ACCENT_COLOR = GREEN_C
NODE_COLOR = GREY_E
EDGE_COLOR = GREY_B

class GraphColouringIntro(MovingCameraScene):
    def construct(self):
        title = Tex("Graph Colouring Algorithms", color=TITLE_COLOR).scale(1.3)
        subtitle = Tex("3821 Project", color=SUBTITLE_COLOR).scale(0.9)

        header = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        bg_box = SurroundingRectangle(header, buff=0.5, color=ACCENT_COLOR, corner_radius=0.2)

        self.play(FadeIn(header, shift=UP, run_time=1.2))
        self.play(Create(bg_box, run_time=1.0))
        self.wait(0.6)

        new_title = Tex("What is Graph Colouring?", color=TITLE_COLOR).scale(1.0)
        new_title.to_corner(UL)

        self.play(
            # self.camera.frame.animate.scale(0.9).shift(UP * 0.5),
            Transform(title, new_title),
            FadeOut(subtitle, shift=DOWN),
            FadeOut(bg_box),
            run_time=1.4
        )
        self.wait(0.5)

        description = Tex(
            "A graph colouring assigns colours to each vertex such that no two adjacent vertices share a colour."
        ).scale(0.8)
        description.set_color_by_tex("colour", SUBTITLE_COLOR)
        description.to_edge(UP).shift(DOWN * 1.5)

        self.play(Write(description), run_time=1.6)
        self.wait(0.8)

        colour_map = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], 4)

        positions = {
            0: LEFT + UP,
            1: RIGHT + UP,
            2: LEFT + DOWN,
            3: RIGHT + DOWN,
        }

        nodes = {}
        for i in range(4):
            circle = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            if i == 2:
                circle.set_fill(colour_map[i - 1])
            else:
                circle.set_fill(colour_map[i])
            circle.move_to(positions[i]).shift(DOWN * 1.5)
            nodes[i] = circle

        edge_pairs = [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]
        edges = []
        for (i, j) in edge_pairs:
            edge = Line(nodes[i].get_center(), nodes[j].get_center(), stroke_width=3, color=EDGE_COLOR)
            edges.append(edge)

        self.play(*[Create(edge) for edge in edges], *[FadeIn(node) for node in nodes.values()])
        self.wait()