import matplotlib.pyplot as plt
from matplotlib import animation
import networkx as nx

def matplotlibAnimation(graph, samples):
    G = nx.from_numpy_array(graph.adjMatrix)
    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(6, 5))

    def update(frame):
        ax.clear()
        ax.set_title(f"Step {frame}")
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_nodes(G, pos, node_color=samples[frame], cmap=plt.cm.Spectral, ax=ax)

    anim = animation.FuncAnimation(fig, update, frames=len(samples), interval=50, repeat=False)
    plt.show()