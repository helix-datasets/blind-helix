import json
import itertools

with open("ground-truth.json", "r") as f:
    data = json.load(f)

total = len(data) * (len(data) - 1) / 2

pairwise = []
for i, (first, second) in enumerate(itertools.combinations(data, 2)):

    def fetch(key):
        return set([t[1] for t in data[key] if t[0] == "function"])

    f, s = [fetch(k) for k in [first, second]]

    similarity = len(f & s) / len(f | s)

    pairwise.append({"first": first, "second": second, "similarity": similarity})

    print(f"\rProgress: {(i+1)/total:.1%}", end="")

print()

with open("ground-truth-pairwise.json", "w") as f:
    json.dump(pairwise, f)
