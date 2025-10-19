from manim import * 
import numpy as np
import networkx as nx

# from graph import Graph
def manimAnimation(graph, samples):
    class GraphColouringAnimation(Scene):
        def construct(self):
            G = nx.from_numpy_array(graph.adjMatrix)
            pos = nx.spring_layout(G, seed=42)

            scale = 3
            pos = {n: np.array([p[0], p[1], 0]) * scale for n, p in pos.items()}

            colour_map = [BLUE, GREEN, RED, ORANGE, PURPLE, YELLOW, TEAL, PINK, GOLD, MAROON]

            nodes = {}
            for i in range(graph.size):
                node_colour = colour_map[samples[0][i] % len(colour_map)]
                circle = Circle(radius=0.2, color=WHITE, fill_opacity=1).move_to(pos[i])
                circle.set_fill(node_colour)
                nodes[i] = circle

            edges = []
            for i in range(graph.size):
                for j in graph.neighbors(i):
                    if j > i:
                        edge = Line(pos[i], pos[j], stroke_width=2, color=GRAY)
                        edges.append(edge)

            self.play(*[Create(edge) for edge in edges], *[FadeIn(node) for node in nodes.values()])
            self.wait(0.5)

            for i in range(1, len(samples), 2):
                animations = []
                for j in range(graph.size):
                    new_colour = colour_map[samples[i][j] % len(colour_map)]
                    if nodes[j].get_fill_color() != new_colour:
                        animations.append(nodes[j].animate.set_fill(new_colour, 1))
                if animations:
                    self.play(*animations, run_time=0.1)
                else:
                    self.wait(0.1)

            self.wait(1)

    return GraphColouringAnimation
