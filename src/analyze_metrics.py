import json
import pandas as pd
import matplotlib.pyplot as plt

def analyze_metrics(filename="match_metrics.jsonl"):
    data = [json.loads(line) for line in open(filename)]
    df = pd.DataFrame(data)

    print("\nBasic Stats:")
    print(df.groupby("role")["score"].describe())

    plt.figure()
    plt.title("Score Progression per Turn")
    plt.plot(df["turn"], df["score"], marker="o")
    plt.xlabel("Turn")
    plt.ylabel("Score")
    plt.show()