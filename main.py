import simulator as sim
import numpy as np
import argparse


def multirun(file, simul, functions, minn=1000, maxi=50000, iterations=1):
    """ Runs a simulation multiple times."""
    with open(file, 'w+') as f:
        for i in np.linspace(minn, maxi, 50):
            for j in np.linspace(minn, maxi, 50):
                print(str(i) + " "+  str(j))
                res = 0
                for _ in range(iterations):
                    simul.reset(variables={'power1': i, 'power2': j})
                    res += run(simul, functions)
                res /= iterations
                f.write(str(i) + ' ' + str(j) + ' ' + str(res) + '\n')


def run(simul, functions):
    """ Run a simulation one time."""
    while simul.step():
        for func in functions:
            func()

    return simul.get_results()


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
                        help='The place where you want to store your results (default=%(default)s).\n\
                        Also if this not set it will not save the results')
    parser.add_argument('--simul_time', type=float, default=20.0,
                        help='The simulation time in seconds every run gets before resulting in failure (default=%(default)d)')
    parser.add_argument('--human_length', type=int, default=160,
                        help='This will give the length of the human that is used in the simulator in cm. (default=%(default)d)')
    parser.add_argument('--human_mass', type=int, default=55,
                        help='This will give the weight of the human that is used in the simulator in kg (default=%(default)d)')
    parser.add_argument('-d', '--debug_view', action='store_true',
                        help='Turn on the visuals using pygame.')
    parser.add_argument('-s', action='store_true',
                        help='Run the simulation only once, do not save the results.')

    args = parser.parse_args()
    functionlist = []
    simul = sim.simulator(args.file, args.simul_time, args.human_length,
                          args.human_mass)

    if args.debug_view:
        import debug

        deb = debug.Debug(simul)
        functionlist.append(deb.step_draw)

    if args.r is "":
        args.r = 'results/' + args.file.split('/')[-1][:-4] + '.res'

    if not args.s:
        multirun(args.r, simul, functionlist, iterations=args.t)
    else:
        run(simul, functionlist)
