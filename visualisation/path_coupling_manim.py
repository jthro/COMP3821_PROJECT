#!/usr/bin/env python3

from manim import *
import numpy as np
import networkx as nx

def manimPathCouplingAnimation(graph, x_samples, y_samples, distances, k):
    class PathCouplingAnimation(Scene):
        def construct(self):
            colour_map = color_gradient(
                [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE],
                max(k, 2)
            )

            G = nx.from_numpy_array(graph.adjMatrix)
            base_pos = nx.kamada_kawai_layout(G)

            scale = 2.5
            left_shift = np.array([-3.5, 0, 0])
            right_shift = np.array([3.5, 0, 0])

            pos_left = {
                n: np.array([p[0], p[1], 0]) * scale + left_shift
                for n, p in base_pos.items()
            }
            pos_right = {
                n: np.array([p[0], p[1], 0]) * scale + right_shift
                for n, p in base_pos.items()
            }

            nodes_left = {}
            nodes_right = {}
            for i in range(graph.size):
                colour_x = colour_map[x_samples[0][i] % len(colour_map)]
                colour_y = colour_map[y_samples[0][i] % len(colour_map)]

                circle_x = Circle(
                    radius=0.25, color=WHITE, fill_opacity=1
                ).move_to(pos_left[i])
                circle_x.set_fill(colour_x)

                circle_y = Circle(
                    radius=0.25, color=WHITE, fill_opacity=1
                ).move_to(pos_right[i])
                circle_y.set_fill(colour_y)

                nodes_left[i] = circle_x
                nodes_right[i] = circle_y

            edges_left = []
            edges_right = []
            for i in range(graph.size):
                for j in graph.neighbors(i):
                    if j > i:
                        edges_left.append(
                            Line(pos_left[i], pos_left[j],
                                 stroke_width=3, color=GRAY)
                        )
                        edges_right.append(
                            Line(pos_right[i], pos_right[j],
                                 stroke_width=3, color=GRAY)
                        )

            bridges = [
                DashedLine(
                    pos_left[i], pos_right[i],
                    stroke_width=1,
                    dash_length=0.1,
                    color=GRAY,
                )
                for i in range(graph.size)
            ]

            left_label = Text("Chain X", font_size=30).next_to(
                VGroup(*nodes_left.values()), UP
            )
            right_label = Text("Chain Y", font_size=30).next_to(
                VGroup(*nodes_right.values()), UP
            )

            step_text = Text("Step: 0", font_size=30).to_corner(UP + LEFT)
            distance_text = Text(
                f"Distance: {distances[0]}",
                font_size=30
            ).to_corner(UP + RIGHT)
            explanation = Text(
                "Yellow pairs = different colours",
                font_size=26
            ).to_edge(DOWN)

            diff_rects = {}
            for i in range(graph.size):
                if x_samples[0][i] != y_samples[0][i]:
                    rect = SurroundingRectangle(
                        VGroup(nodes_left[i], nodes_right[i]),
                        buff=0.15,
                        color=YELLOW,
                        stroke_width=4,
                    )
                    diff_rects[i] = rect

            self.add(*edges_left, *edges_right, *bridges)
            self.add(*nodes_left.values(), *nodes_right.values())
            self.add(left_label, right_label, step_text, distance_text, explanation)
            self.add(*diff_rects.values())
            self.wait(0.5)

            coupled_shown = False
            coupled_label = None

            for t in range(1, len(x_samples)):
                self.remove(step_text, distance_text)
                step_text = Text(
                    f"Step: {t}",
                    font_size=30
                ).to_corner(UP + LEFT)
                distance_text = Text(
                    f"Distance: {distances[t]}",
                    font_size=30
                ).to_corner(UP + RIGHT)
                self.add(step_text, distance_text)

                animations = []
                for i in range(graph.size):
                    new_colour_x = colour_map[x_samples[t][i] % len(colour_map)]
                    new_colour_y = colour_map[y_samples[t][i] % len(colour_map)]

                    if nodes_left[i].get_fill_color() != new_colour_x:
                        animations.append(
                            nodes_left[i].animate.set_fill(new_colour_x, 1)
                        )
                    if nodes_right[i].get_fill_color() != new_colour_y:
                        animations.append(
                            nodes_right[i].animate.set_fill(new_colour_y, 1)
                        )

                for rect in diff_rects.values():
                    self.remove(rect)
                diff_rects = {}
                for i in range(graph.size):
                    if x_samples[t][i] != y_samples[t][i]:
                        rect = SurroundingRectangle(
                            VGroup(nodes_left[i], nodes_right[i]),
                            buff=0.15,
                            color=YELLOW,
                            stroke_width=4,
                        )
                        diff_rects[i] = rect
                self.add(*diff_rects.values())

                if distances[t] == 0 and not coupled_shown:
                    coupled_label = Text(
                        "Chains have coupled!",
                        font_size=32,
                        color=GREEN,
                    ).next_to(explanation, UP)
                    self.play(Write(coupled_label))
                    coupled_shown = True

                if animations:
                    self.play(*animations, run_time=0.2)
                else:
                    self.wait(0.2)

            self.wait(1)

    return PathCouplingAnimation
