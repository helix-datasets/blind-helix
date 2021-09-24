import json
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compute averaged performance")

    parser.add_argument("performance", nargs="+", help="performance files (json)")

    parser.add_argument(
        "-o", "--output", help="output file to write results (default: stdout)"
    )

    arguments = parser.parse_args()

    performances = []
    for perf in arguments.performance:
        with open(perf, "r") as f:
            performances.append(json.load(f))

    performance = {}
    for k in performances[0]:
        performance[k] = sum([p[k] for p in performances]) / len(performances)

    if arguments.output:
        with open(arguments.output, "w") as f:
            json.dump(performance, f)
    else:
        print("Ranking:")
        for i, name in enumerate(sorted(performance, key=performance.get)):
            print(f"{i+1}. {name} ({performance[name]:.4})")
