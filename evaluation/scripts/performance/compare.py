import os
import json
import argparse

from sklearn import metrics


def align(*args):
    keys = None

    for a in args:
        if keys is not None:
            keys &= set(a.keys())
        else:
            keys = set(a.keys())

    return [[a[k] for k in keys] for a in args]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="compare ground truth to similarity scores"
    )

    parser.add_argument("labels", help="ground truth labels (json)")
    parser.add_argument(
        "scores", nargs="+", help="predicted similarity score files (json)"
    )

    parser.add_argument(
        "-n",
        "--naive",
        type=float,
        default=None,
        help="add a naive metric that always estimates the same value",
    )

    parser.add_argument(
        "-o", "--output", help="output file to write results (default: stdout)"
    )

    arguments = parser.parse_args()

    def load(path):
        with open(path, "r") as f:
            data = json.load(f)

        data = {tuple(sorted((d["first"], d["second"]))): d["similarity"] for d in data}

        return data

    labels = load(arguments.labels)

    scores = {}
    for score in arguments.scores:
        name = os.path.splitext(os.path.basename(score))[0]
        scores[name] = load(score)

    aligned = align(labels, *[scores[n] for n in sorted(scores)])

    labels = aligned[0]
    scores = dict(zip(sorted(scores), aligned[1:]))

    if arguments.naive is not None:
        scores["naive"] = [arguments.naive] * len(labels)

    performance = {}
    for name, score in scores.items():
        # performance[name] = metrics.mean_absolute_error(labels, score)
        performance[name] = metrics.mean_squared_error(labels, score, squared=False)

    if arguments.output:
        with open(arguments.output, "w") as f:
            json.dump(performance, f)
    else:
        print("Ranking:")
        for i, name in enumerate(sorted(performance, key=performance.get)):
            print(f"{i+1}. {name} ({performance[name]:.4})")
