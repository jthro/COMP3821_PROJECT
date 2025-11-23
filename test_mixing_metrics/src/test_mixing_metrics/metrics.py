from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


def aggregate_metric(entries, metric_key):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for e in entries:
        chain = e["chain_name"]
        shape = e["shape"]
        nv = e["nv"]
        value = e[metric_key]
        table[chain][shape][nv].append(value)

    stats = {}
    for chain, ks in table.items():
        stats[chain] = {}
        for k, nv_dict in ks.items():
            nvs = sorted(nv_dict.keys())
            means = [np.mean(nv_dict[nv]) for nv in nvs]
            stds = [
                np.std(nv_dict[nv], ddof=1) / np.sqrt(len(nv_dict[nv])) for nv in nvs
            ]
            stats[chain][k] = (nvs, means, stds)

    return stats


DEFAULT_COLOURS = {"middleton-bulseco": "blue", "naive-metropolis": "red"}


def plot_metric(stats, metric_name, colours=DEFAULT_COLOURS):
    all_ks = sorted({k for chain in stats.values() for k in chain.keys()}, key=str)

    fig, axes = plt.subplots(len(all_ks), 1, figsize=(8, 4 * len(all_ks)), sharex=True)

    if len(all_ks) == 1:
        axes = [axes]

    for ax, k in zip(axes, all_ks):
        ax.set_title(f"Mean Steps to First Colouring vs. |V| ({k})")

        for chain, chain_stats in stats.items():
            if k not in chain_stats:
                continue

            nvs, means, stds = chain_stats[k]

            ax.errorbar(
                nvs,
                means,
                yerr=stds,
                marker="o",
                capsize=4,
                label=chain,
                color=colours.get(chain, None),
            )

        ax.set_ylabel("Time to First Colouring")
        ax.legend()

    axes[-1].set_xlabel("|V|")
    plt.tight_layout()
    plt.show()
