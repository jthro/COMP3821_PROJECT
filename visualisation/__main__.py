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
    parser.add_argument("--size", required=True)
    parser.add_argument("--steps", required=True)

    args = parser.parse_args()

    module = importlib.import_module(f"visualisation.algorithms.{args.algo}")
    function = getattr(module, args.algo)

    g = Graph(int(args.size))
    for _ in range(random.randint(int(g.size * 1.5), int(g.size * 2))):
        v1, v2 = random.sample(range(g.size), 2)
        g.add_edge(v1, v2)

    k = g.size
    num_steps = int(args.steps)
    start_colouring = np.random.randint(0, k, g.size)
    samples = function(g, k, num_steps, start_colouring)

    if args.visualiser == "manim":
        SceneClass = manimAnimation(g, samples, k)
        scene = SceneClass()
        scene.render() 
    else:
        matplotlibAnimation(g, samples, k)

if __name__ == "__main__":
    main()
