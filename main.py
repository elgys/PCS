import exercise_interpreter as inter
import numpy as np
import argparse

def results(file):
    with open(file, 'w+') as f:
        for i in np.logspace(3, 6, 50):
            for j in np.logspace(3, 6, 50):
                f.write(str(i) + ' ' + str(j) + ' ' + str(simul.run_simulation(
                    variables={'power1': i, 'power2': j})) + '\n')

if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description='Process an exercise according to a given .exc file.')
    parser.add_argument('--file', type=str, default='./exercises/T_pose.exc',
                        help='The name of the file to be simulated (default=%(default)s)')
    parser.add_argument('-t', type=int, default=1, metavar='N',
                        help='Amount of times to simulate the current file (default=%(default)d)')
    parser.add_argument('-r', type=str, default='./results/default_results.res',
                        help='The place where you want to store your results (default=%(default)s).\n\
                        Also if this not set it will not save the results')
    parser.add_argument('--simul_time', type=float, default=20.0,
                        help='The simulation time in seconds every run gets before resulting in failure (default=%(default)d)')

    args = parser.parse_args()

    simul = inter.Exercise_simulator(args.file, args.t, args.simul_time)


    if args.r is not "":
        results(args.r)
