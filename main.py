import exercise_interpreter as inter
import numpy as np
import argparse


def results(file, simul):
    """ Create a .res file with all results of multiple simulations."""
    with open(file, 'w+') as f:
        for i in np.linspace(1000, 50000, 50):
            for j in np.linspace(1000, 50000, 50):
                f.write(str(i) + ' ' + str(j) + ' ' + str(simul.run_simulation(
                    variables={'power1': i, 'power2': j})) + '\n')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Process an exercise according to a given .exc file.\n\
                     Standard the exercise is run with forces from the arm and leg\n\
                     ranging from 1000 to 50000.')
    parser.add_argument('--file', type=str, default='./exercises/T_pose.exc',
                        help='The name of the file to be simulated (default=%(default)s)')
    parser.add_argument('-t', type=int, default=1, metavar='N',
                        help='Amount of times to simulate the current file per power pair.\n\
                        After some testing, the models seem deterministic, \n\
                        so more than once should not be necessary.\n\
                        (default=%(default)d)')
    parser.add_argument('-r', type=str, default='',
                        help='The place where you want to store your results (default=./results/<name exc file>.res')
    parser.add_argument('--simul_time', type=float, default=20.0,
                        help='The simulation time in seconds every run gets before resulting in failure (default=%(default)d)')
    parser.add_argument('-v', action='store_true',
                        help='Turn visualization on')
    parser.add_argument('-s', action='store_true',
                        help='Only simulate a single scenario and do not save results.')

    args = parser.parse_args()

    simul = inter.Exercise_simulator(
        args.file, args.t, args.simul_time, visual=args.v)

    if args.r == '':
        args.r = './results/' + args.file.split('/')[-1][:-4] + '.res'

    if not args.s:
        results(args.r, simul)
    else:
        print(simul.run_simulation(
            variables={'power1': 25000, 'power2': 25000}) / np.pi * 180)
