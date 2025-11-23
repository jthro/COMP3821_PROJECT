from manim import *
import numpy as np
import networkx as nx

def manimCouplingAnimation(graph, x_samples, y_samples, distances, k):

    class PathCouplingAnimation(Scene):
        def construct(self):
            colour_map = color_gradient(
                [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], k
            )

            G = nx.from_numpy_array(graph.adjMatrix)
            pos = nx.kamada_kawai_layout(G)
            scale = 3
            pos = {n: np.array([p[0], p[1], 0]) * scale for n, p in pos.items()}

            left_shift = LEFT * 4
            right_shift = RIGHT * 4

            x_nodes = {}
            y_nodes = {}
            for i in range(graph.size):
                colX = colour_map[x_samples[0][i] % k]
                circleX = Circle(radius=0.25, color=WHITE, fill_opacity=1)
                circleX.move_to(pos[i] + left_shift)
                circleX.set_fill(colX)
                x_nodes[i] = circleX

                colY = colour_map[y_samples[0][i] % k]
                circleY = Circle(radius=0.25, color=WHITE, fill_opacity=1)
                circleY.move_to(pos[i] + right_shift)
                circleY.set_fill(colY)
                y_nodes[i] = circleY

            x_edges = []
            y_edges = []
            for i in range(graph.size):
                for j in graph.neighbors(i):
                    if j > i:
                        edgeX = Line(
                            pos[i] + left_shift,
                            pos[j] + left_shift,
                            stroke_width=2,
                            color=GRAY
                        )
                        edgeY = Line(
                            pos[i] + right_shift,
                            pos[j] + right_shift,
                            stroke_width=2,
                            color=GRAY
                        )
                        x_edges.append(edgeX)
                        y_edges.append(edgeY)

            titleX = Text("Chain X", font_size=36).move_to(UP * 3 + left_shift)
            titleY = Text("Chain Y", font_size=36).move_to(UP * 3 + right_shift)

            distance_text = Text(
                f"Distance: {distances[0]}", font_size=32
            ).to_edge(DOWN)

            self.play(
                *[Create(e) for e in x_edges],
                *[Create(e) for e in y_edges],
                *[FadeIn(n) for n in x_nodes.values()],
                *[FadeIn(n) for n in y_nodes.values()],
                FadeIn(titleX), FadeIn(titleY),
                FadeIn(distance_text)
            )
            self.wait(0.5)

            for t in range(1, len(x_samples)):

                frames = []

                for i in range(graph.size):
                    colX = colour_map[x_samples[t][i] % k]
                    frames.append(x_nodes[i].animate.set_fill(colX))

                for i in range(graph.size):
                    colY = colour_map[y_samples[t][i] % k]
                    frames.append(y_nodes[i].animate.set_fill(colY))

                new_distance = distances[t]
                new_text = Text(
                    f"Distance: {new_distance}", font_size=32
                ).to_edge(DOWN)

                self.remove(distance_text)
                distance_text = new_text
                self.add(distance_text)

                self.play(*frames, run_time=0.1)

            self.wait(1)

    return PathCouplingAnimation
