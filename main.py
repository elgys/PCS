import simulator as sim
import debug
import numpy as np
import argparse

def results(file):
    with open(file, 'w+') as f:
        for i in np.logspace(3, 6, 50):
            for j in np.logspace(3, 6, 50):
                f.write(str(i) + ' ' + str(j) + ' ' + str(simul.run_simulation(
                    variables={'power1': i, 'power2': j})) + '\n',visual=args.d)


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
    parser.add_argument('--human_size',type=int, default = 160,
                        help='This will give the humans size that be used for the sim. (default=%(default)d)')
    parser.add_argument('--human_weight',type=int,default=55,
                        help='This will give the weight of a human (default=%(default)d)')
    parser.add_argument('-d','--debug_view',action='store_true',help ='Here we will call \
                        upon the drwing of pygame and pymunk is usefull for debug drawing')

    args = parser.parse_args()

    simul = sim.simulator(args.file, args.t,
                                     args.simul_time,
                                     args.human_size,
                                     args.human_weight,
                                     visual=args.debug_view)
    if args.r is not "":
        results(args.r)
