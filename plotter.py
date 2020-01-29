import matplotlib.pyplot as plt
import numpy as np


def main(X, Y, Z, title=None):
    """ Create a heatmap of the results."""
    Z = Z * 180 / np.pi

    fig, ax = plt.subplots()
    heatmap = ax.imshow(Z, cmap='gray', interpolation='none', extent=[
                        min(X), max(X), min(Y), max(Y)], origin='lower')
    cbar = fig.colorbar(heatmap, ax=ax, extend='max')

    cbar.set_label("Degrees turned")
    ax.set_xlabel("Power leg (N)")
    ax.set_ylabel("Power hand (N)")

    if title:
        ax.set_title(str(title) + " position")

    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Plot a res file in a heatmap.')
    parser.add_argument('file', type=str, default='./results/T_pose.res',
                        help='The name of the file to be plotted (default=%(default)s)')

    args = parser.parse_args()
    filename = args.file
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

    main(np.array(X, dtype=float) / 100, np.array(
         Y, dtype=float) / 100, np.array(Z, dtype=float),
         title=(filename.split('/')[-1][:-4]).replace('_', ' '))
