from matplotlib import pyplot as plt
import numpy as np

def make_bars(
        x,
        y,
        width,
):
    xs = [x[0] - width]
    ys = [0]
    for i in range(len(x)):
        xs.append(x[i] - width)
        xs.append(x[i] + width)
        ys.append(y[i])
        ys.append(y[i])
    xs.append(x[-1] + width)
    ys.append(y[-1])

    return xs, ys


def plot_hist(
        data_set,
        labels,
        color,
        style,
        title,
        box_n,
        range,
):
    plt.figure(figsize=(10, 10))
    plt.title(title)
    for i, data in enumerate(data_set):
        weg = np.ones_like(data) / float(len(data))
        results, edges = np.histogram(data, range=(0, range), weights=weg, bins=box_n, density=1, )
        binWidth = edges[1] - edges[0]
        xs, ys = make_bars(edges[:-1], results * binWidth, binWidth / 2)

        plt.plot(xs, ys, label=labels[i], color=color[i], linestyle=style[i], linewidth=2)
    plt.grid()
    plt.xlim(0, range)
    #plt.ylim(0, 1)
    plt.show()
    return