import os
import json
import argparse
import itertools


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="similarity comparison worksheet")

    parser.add_argument("output", help="output labels JSON file")
    parser.add_argument(
        "files", metavar="FILE", nargs="+", help="files to include in comparison"
    )

    arguments = parser.parse_args()

    data = []
    if os.path.isfile(arguments.output):
        with open(arguments.output, "r") as f:
            data = json.load(f)

    data = {(d["first"], d["second"]): d["similarity"] for d in data}

    try:
        for first, second in itertools.combinations(arguments.files, 2):
            if (first, second) in data or (second, first) in data:
                continue

            score = None

            while score is None:
                score = input(f"{first} vs {second}: ")

                try:
                    score = float(score)

                    if score > 1.0 or score < 0.0:
                        raise ValueError
                except ValueError:
                    print(f"invalid similarity score: {score}")

                    score = None

            data[(first, second)] = score
    except (KeyboardInterrupt, EOFError):
        print()
    else:
        print("worksheet complete")

    data = [{"first": k[0], "second": k[1], "similarity": v} for k, v in data.items()]

    with open(arguments.output, "w") as f:
        json.dump(data, f)

    print(f"wrote results to {arguments.output}")
