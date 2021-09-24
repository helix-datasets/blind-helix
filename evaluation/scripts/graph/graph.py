import json
import argparse

import numpy
from matplotlib import pyplot

NAME_MAP = {
    "ssdeep": "ssdeep",
    "sdhash": "sdhash",
    "lzjd": "LZJD",
    "tlsh": "TLSH",
    "bindiff": "BinDiff",
    "naive": "naive",
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="graph a thing")

    parser.add_argument(
        "performance", nargs="+", help="performance metric file(s) (json)"
    )
    parser.add_argument(
        "-b",
        "--bar-labels",
        action="store_true",
        default=False,
        help="enable bar labels",
    )

    arguments = parser.parse_args()

    performances = {}
    for p in arguments.performance:
        name, f = p.split(":")

        with open(f, "r") as f:
            performances[name] = json.load(f)

    pyplot.rcParams["font.family"] = "Roboto"
    pyplot.rcParams["font.size"] = 12
    pyplot.rcParams["axes.linewidth"] = 2

    fig, ax = pyplot.subplots()
    cmap = pyplot.get_cmap("Pastel2")

    average = {}
    for name, performance in performances.items():
        for metric, value in performance.items():
            if metric not in average:
                average[metric] = []
            average[metric].append(value)

    average = {k: sum(v) / len(v) for k, v in average.items()}
    ranked = sorted(average, key=performance.get, reverse=True)
    ranked = ["ssdeep", "sdhash", "lzjd", "tlsh", "naive", "bindiff"]
    index = numpy.arange(len(ranked))

    width = (0.8) / len(performances)

    for i, (name, performance) in enumerate(performances.items()):
        bars = ax.bar(
            index + (i - (len(performances) - 1) / 2) * width,
            [performance[k] for k in ranked],
            width,
            color=cmap(i),
            edgecolor="black",
            label=name.replace("-", " ").title(),
        )

        if arguments.bar_labels:
            ax.bar_label(bars, padding=3, fmt="%.2f")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks(index)
    ax.set_xticklabels([NAME_MAP[n] for n in ranked])
    ax.legend(frameon=False)

    ax.xaxis.set_tick_params(bottom=False, top=False)
    ax.yaxis.set_tick_params(which="major", size=8, width=2, direction="in")

    pyplot.ylabel("Performance (MAE)", labelpad=10)
    pyplot.ylim((0, 1))
    pyplot.xlabel("Metric", labelpad=10)

    fig.tight_layout()

    pyplot.show()
