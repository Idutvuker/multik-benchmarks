import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (20, 10)

SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 24

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


def bar_chart(data, title):
    labels = ["multikCuda", "multikCudaCTH", "multikNative", "Nd4j"]
    shapes = pd.unique(data["(shapeStr)"])

    # gbShape = data.groupby("(shapeStr)")
    gb_func = data.groupby("Benchmark")

    scores = np.zeros((len(labels), len(shapes)))

    for i, group in enumerate(gb_func):
        scores[i] = group[1]["Score"]

    ratio = scores / scores[2]

    df = pd.DataFrame(ratio.T, columns=labels, index=shapes)

    x_ticks = np.arange(len(shapes))
    offset = np.linspace(-0.3, 0.3, len(labels))

    fig, ax = plt.subplots()

    formatter = lambda x: f'{x:4.2f} op/s'

    for i, column in enumerate(df):
        rect = ax.bar(x_ticks + offset[i], df[column], width=0.15, label=column)
        ax.bar_label(rect, labels=map(formatter, scores[i]), rotation="vertical", label_type="center")

    ax.set_ylabel('Ratio')
    ax.set_xlabel('Shape')

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(shapes)
    ax.legend()
    ax.grid()
    ax.set_title(title)

    fig.savefig(f"{title.replace(' ', '')}.png", bbox_inches='tight')


def main():
    data1 = pd.read_csv("data/square.txt", sep="\\s+")

    bar_chart(data1, "Square Matrix Multiplication")
    # bar_chart(data1, "Rectangular Matrix Multiplication")


main()
