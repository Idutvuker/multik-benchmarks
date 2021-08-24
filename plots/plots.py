import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from io import StringIO

plt.rcParams['figure.dpi'] = 140
plt.rcParams["figure.figsize"] = (16, 9)

SMALL_SIZE = 14
MEDIUM_SIZE = 14
BIGGER_SIZE = 24

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


def bar_chart(data, title, step=1.0, fontsize=9):
    labels = ["multikCuda", "multikCudaCTH", "multikNative", "Nd4j"]
    shapes = pd.unique(data["(shapeStr)"])

    # gbShape = data.groupby("(shapeStr)")
    gb_func = data.groupby("Benchmark")

    scores = np.zeros((len(labels), len(shapes)))

    for i, group in enumerate(gb_func):
        scores[i] = group[1]["Score"]

    ratio = scores / scores[2]

    df = pd.DataFrame(ratio.T, columns=labels, index=shapes)

    x_ticks = np.arange(len(shapes)) * step
    offset = np.linspace(-step/3, step/3, len(labels))

    fig, ax = plt.subplots()

    formatter = lambda x: f'{x:4.2f} op/s'

    for i, column in enumerate(df):
        rect = ax.bar(x_ticks + offset[i], df[column], width=step/6, label=column)
        bar_labels = ax.bar_label(rect, labels=map(formatter, scores[i]), rotation="vertical", label_type="edge", fontsize=fontsize, padding=5)
        for label in bar_labels:
            label.xy = (label.xy[0], 0)

    ax.set_ylabel('Ratio')
    ax.set_xlabel('Shape')

    ax.set_yticks(np.arange(np.max(ratio)))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(shapes, rotation='45')
    ax.legend()
    ax.grid(axis='y')
    ax.set_title(title)

    fig.savefig(f"{title.replace(' ', '')}.png", bbox_inches='tight')


def main():
    data1 = pd.read_csv("data/square.txt", sep="\\s+")
    bar_chart(data1, "Square Matrix Multiplication", fontsize=12)

    data2 = pd.read_csv("data/nonsquare.txt", sep="\\s+")
    bar_chart(data2, "Rectangular Matrix Multiplication", fontsize=9)


main()
