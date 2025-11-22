from manim import * 
import numpy as np
import networkx as nx

# from graph import Graph
def manimAnimation(graph, samples, k):
    class GraphColouringAnimation(Scene):
        def construct(self):
            colour_map = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], k)

            G = nx.from_numpy_array(graph.adjMatrix)
            pos = nx.kamada_kawai_layout(G)

            scale = 3
            pos = {n: np.array([p[0], p[1], 0]) * scale for n, p in pos.items()}

            nodes = {}
            for i in range(graph.size):
                node_colour = colour_map[samples[0][i] % len(colour_map)]
                circle = Circle(radius=0., color=WHITE, fill_opacity=1).move_to(pos[i])
                circle.set_fill(node_colour)
                nodes[i] = circle

            edges = []
            for i in range(graph.size):
                for j in graph.neighbors(i):
                    if j > i:
                        edge = Line(pos[i], pos[j], stroke_width=3, color=GRAY)
                        edges.append(edge)

            number = Text(f"Frame: 0", font_size=36).to_corner(UP + RIGHT)
            self.add(number)
            conflicts = Text(f"Conflicts: {graph.check_num_conflicts(samples[0])}", font_size=36).to_corner(UP + LEFT)
            self.add(conflicts)
            max_degree = Text(f"Max Degree: {graph.check_max_degree()}", font_size=36).to_corner(DOWN + LEFT)
            self.add(max_degree)
            num_colours = Text(f"Current colours: {graph.check_num_colours(samples[0])} Min colours: null", font_size=36).to_corner(DOWN + RIGHT)
            self.add(num_colours)

            least_colours = "null"

            self.play(*[Create(edge) for edge in edges], *[FadeIn(node) for node in nodes.values()])
            self.wait(0.5)

            for i in range(len(samples) - 1):
                self.remove(number)
                number = Text(f"Frame: {i}", font_size=36).to_corner(UP + RIGHT)
                self.add(number)

                self.remove(conflicts)
                conflicts = Text(f"Conflicts: {graph.check_num_conflicts(samples[i])}", font_size=36).to_corner(UP + LEFT)
                self.add(conflicts)

                if (graph.check_num_conflicts(samples[i]) == 0):
                    if (least_colours == "null"):
                        least_colours = graph.check_num_colours(samples[i])
                    elif (graph.check_num_colours(samples[i]) < least_colours):
                        least_colours = graph.check_num_colours(samples[i])

                self.remove(num_colours)
                num_colours = Text(f"Current colours: {graph.check_num_colours(samples[i])} Min colours: {least_colours}", font_size=36).to_corner(DOWN + RIGHT)
                self.add(num_colours)

                
                animations = []
                for j in range(graph.size):
                    new_colour = colour_map[samples[i][j] % len(colour_map)]
                    if nodes[j].get_fill_color() != new_colour:
                        animations.append(nodes[j].animate.set_fill(new_colour, 1))
                if animations:
                    self.play(*animations, run_time=0.1)
                else:
                    self.wait(0.1)

            # least = Text(f"Min colours: {least_colours}", fon)
            # self.add(least)
            # self.wait(3)

    return GraphColouringAnimation
