import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def main(X, Y, Z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # X, Y, Z = [1, 2], [3, 4], np.array([[5, 6], [7, 8]])
    X = np.log10(X)
    Y = np.log10(Y)
    Z = Z * 180 / np.pi
    ax.plot_wireframe(X, Y, Z)
    ticks = [10 ** i for i in range(3, 7)]
    ax.set_xticks(np.log10(ticks))
    ax.set_xticklabels(ticks)
    ax.set_yticks(np.log10(ticks))
    ax.set_yticklabels(ticks)
    ax.set_xlabel("Power leg")
    ax.set_ylabel("Power hand")
    ax.set_zlabel("Degrees turned")
    plt.show()


def main():
    pass


if __name__ == "__main__":
    filename = './results/default_results.res'
    X, Y, Z = [], [], []
    with open(filename) as f:
        for line in f:
            x, y, z = line.split()
            if x not in X:
                X.append(x)
                Z.append([])
            if y not in Y:
                Y.append(y)
            Z[-1].append(z)
    X, Y = np.meshgrid(X, Y)
    main(np.array(X, dtype=float), np.array(
        Y, dtype=float), np.array(Z, dtype=float))
