# visualisation/__main__.py
import argparse
import importlib
import random
import numpy as np

from .graph import Graph
from .manimAnimation import manimAnimation
from .matplotlibAnimation import matplotlibAnimation

def main():
    parser = argparse.ArgumentParser(description="3821 Visualisations")
    parser.add_argument("--algo", required=True)
    parser.add_argument("--visualiser", required=True)
    args = parser.parse_args()

    module = importlib.import_module(f"visualisation.algorithms.{args.algo}")
    function = getattr(module, args.algo)

    g = Graph(random.randint(5, 10))
    for _ in range(random.randint(10, 25)):
        v1, v2 = random.sample(range(g.size), 2)
        g.add_edge(v1, v2)

    k = g.size
    num_steps = 15
    start_colouring = np.random.randint(0, k, g.size)
    samples = function(g, k, num_steps, start_colouring)

    if args.visualiser == "manim":
        SceneClass = manimAnimation(g, samples)
        scene = SceneClass()
        scene.render() 
    else:
        matplotlibAnimation(g, samples)

if __name__ == "__main__":
    main()
