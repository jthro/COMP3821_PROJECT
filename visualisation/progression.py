from manim import *

TITLE_COLOR = GREEN_E
SUBTITLE_COLOR = GREY_B
ACCENT_COLOR = GREEN_C
NODE_COLOR = GREY_E
EDGE_COLOR = GREY_B

class GraphCreation(Scene):
    def construct(self):
        colour_map = color_gradient([RED, BLUE], 2)

        positions = {
            0: UP,
            1: RIGHT + DOWN,
            2: LEFT + DOWN,
        }

        mob = VGroup()

        scale_factor = 0.8
        
        nodes = {}
        for i in range(3):
            circle = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            circle.set_fill(colour_map[0])
            circle.move_to(positions[i]).shift(LEFT * 5)
            nodes[i] = circle
            mob.add(circle)

        edge_pairs = [(0, 1), (0, 2)]
        edges = []
        for i, j in edge_pairs:
            edge = Line(nodes[i].get_center(), nodes[j].get_center(), stroke_width=3, color=EDGE_COLOR)
            edges.append(edge)
            mob.add(edge)

        arrows = [
            Arrow(4 * LEFT, 2 * UL),
            Arrow(4 * LEFT, 2 * LEFT),
            Arrow(4 * LEFT, 2 * DL),
            Arrow(DL * 0.1 + DOWN * 2, RIGHT * 2),
            Arrow(LEFT * 0.1, RIGHT * 2)
        ]

        labels_text = ["0.3", "0.3", "0.3", "0.5", "0.5"]
        labels = []

        for arrow, text in zip(arrows, labels_text):
            mob.add(arrow)
            label = Text(text, font_size=24)
            label.move_to((arrow.get_start() + arrow.get_end()) / 2 + UP * 0.5)
            vec = arrow.get_end() - arrow.get_start()
            angle = np.arctan2(vec[1], vec[0])
            label.rotate(angle)
            labels.append(label)
            mob.add(label)

        nodes2 = {}
        for i in range(3):
            circle = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            circle.set_fill(colour_map[1] if i == 0 else colour_map[0])
            circle.move_to(positions[i]).shift(LEFT).shift(UP * 3)
            nodes2[i] = circle
            mob.add(circle)

        edges2 = []
        for i, j in edge_pairs:
            edge = Line(nodes2[i].get_center(), nodes2[j].get_center(), stroke_width=3, color=EDGE_COLOR)
            edges2.append(edge)
            mob.add(edge)

        loop = CurvedArrow(
            start_point=UP * 2.5 + LEFT * 0.01,
            end_point=UP * 3.5 + LEFT * 0.01,
            angle=TAU / 2,
            tip_length=0.2,
            stroke_width=5,
        )
        mob.add(loop)

        loop_label = Text("1", font_size=24).move_to(UP * 3 + RIGHT)
        mob.add(loop_label)

        nodes3 = {}
        for i in range(3):
            circle = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            circle.set_fill(colour_map[1] if i == 1 else colour_map[0])
            circle.move_to(positions[i]).shift(LEFT)
            nodes3[i] = circle
            mob.add(circle)

        edges3 = []
        for i, j in edge_pairs:
            edge = Line(nodes3[i].get_center(), nodes3[j].get_center(), stroke_width=3, color=EDGE_COLOR)
            edges3.append(edge)
            mob.add(edge)

        nodes4 = {}
        for i in range(3):
            circle = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            circle.set_fill(colour_map[1] if i == 2 else colour_map[0])
            circle.move_to(positions[i]).shift(LEFT).shift(DOWN * 3)
            nodes4[i] = circle
            mob.add(circle)

        edges4 = []
        for i, j in edge_pairs:
            edge = Line(nodes4[i].get_center(), nodes4[j].get_center(), stroke_width=3, color=EDGE_COLOR)
            edges4.append(edge)
            mob.add(edge)

        nodes5 = {}
        for i in range(3):
            circle = Circle(radius=0.3, color=WHITE, fill_opacity=1)
            circle.set_fill(colour_map[1] if i in [1, 2] else colour_map[0])
            circle.move_to(positions[i]).shift(RIGHT * 3)
            nodes5[i] = circle
            mob.add(circle)

        edges5 = []
        for i, j in edge_pairs:
            edge = Line(nodes5[i].get_center(), nodes5[j].get_center(), stroke_width=3, color=EDGE_COLOR)
            edges5.append(edge)
            mob.add(edge)

        loop2 = CurvedArrow(
            start_point=RIGHT * 4 + DOWN * 0.5,
            end_point=RIGHT * 4 + UP * 0.5,
            angle=TAU / 2,
            tip_length=0.2,
            stroke_width=5,
        )
        mob.add(loop2)

        loop_label2 = Text("1", font_size=24).move_to(RIGHT * 5)
        mob.add(loop_label2)

        mob.scale(scale_factor)
        mob.move_to(ORIGIN)

        self.play(*[Create(edge) for edge in edges], *[FadeIn(node) for node in nodes.values()])
        self.wait()

        self.play(GrowArrow(arrows[0]), *[FadeIn(labels[0])])

        self.play(*[Create(edge) for edge in edges2], *[FadeIn(node) for node in nodes2.values()])
        self.wait()

        self.play(Create(loop), FadeIn(loop_label))
        self.play(GrowArrow(arrows[1]), FadeIn(labels[1]))

        self.play(*[Create(edge) for edge in edges3], *[FadeIn(node) for node in nodes3.values()])
        self.wait()
        self.play(GrowArrow(arrows[2]), FadeIn(labels[2]))

        self.play(*[Create(edge) for edge in edges4], *[FadeIn(node) for node in nodes4.values()])
        self.wait()
        self.play(GrowArrow(arrows[3]), FadeIn(labels[3]),
                  GrowArrow(arrows[4]), FadeIn(labels[4]))

        self.play(*[Create(edge) for edge in edges5], *[FadeIn(node) for node in nodes5.values()])
        self.play(Create(loop2), FadeIn(loop_label2))
        self.wait()
