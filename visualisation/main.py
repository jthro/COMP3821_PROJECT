import argparse
import importlib
import random
import numpy as np
import json

from .graph import Graph
from .manimAnimation import manimAnimation
from .matplotlibAnimation import matplotlibAnimation

def main():
    parser = argparse.ArgumentParser(description="3821 Visualisations")
    parser.add_argument("--algo", required=True)
    parser.add_argument("--visualiser", required=True)
    parser.add_argument("--size", required=False)
    parser.add_argument("--steps", required=False)

    args = parser.parse_args()

    if args.algo == "colouring":
        with open("visualisation/colour1.jsonl", "r") as f:
            data = json.loads(f.read())

        samples = data["colourings:"]
        nv = data["nv"]
        k = data["k"]

        g = Graph(nv)
    else:
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
        matplotlibAnimation(g, samples)

if __name__ == "__main__":
    main()
