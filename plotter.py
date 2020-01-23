import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cbook as cbook
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def main(X, Y, Z, title=None):
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    #
    # # X, Y, Z = [1, 2], [3, 4], np.array([[5, 6], [7, 8]])
    # X = np.log10(X)
    # Y = np.log10(Y)
    # Z = Z * 180 / np.pi
    # ax.plot_wireframe(X, Y, Z)
    # ticks = [10 ** i for i in range(3, 7)]
    # ax.set_xticks(np.log10(ticks))
    # ax.set_xticklabels(ticks)
    # ax.set_yticks(np.log10(ticks))
    # ax.set_yticklabels(ticks)
    # ax.set_xlabel("Power leg")
    # ax.set_ylabel("Power hand")
    # ax.set_zlabel("Degrees turned")
    # plt.show()
    # fig, ax = plt.subplots()
    # pcm = ax.pcolor(X, Y, Z,norm=colors.LogNorm(vmin=Z.min(),vmax=Z.max()),cmap='PuBu_r')
    # fig.colorbar(pcm, ax=ax, extend='max')
    # plt.show()
    Z = Z * 180 / np.pi

    cMap = colors.ListedColormap(['red', 'orange', 'green'])
    fig, ax = plt.subplots()
    heatmap = ax.imshow(Z, cmap='gray', interpolation='none', extent=[
                        10, 500, 10, 500], origin='lower')
    cbar = fig.colorbar(heatmap, ax=ax, extend='max')
    # plt.xscale('log')
    # plt.yscale('log')

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
    parser.add_argument('file', type=str, default='./results/default_results.res',
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
    X, Y = np.meshgrid(X, Y)
    main(np.array(X, dtype=float), np.array(
        Y, dtype=float), np.array(Z, dtype=float), title=(filename.split('/')[-1][:-4]).replace('_', ' '))
