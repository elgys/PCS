import wheel_model


class Exercise_simulator:
    def __init__(self, filename, auto_parse=True):
        self.file = filename
        self.parsed = False
        self.angle_actions = []  # [[angle, f, *args]]
        if auto_parse:
            self.parse()

    def parse(self):
        with open(self.file, 'r') as f:
            for line in f:
                self.angle_actions.append(line.split())
        self.parsed = True

    def setup_angle_actions_model(self, model):
        for angle, function, *args in self.angle_actions:
            if function == 'setturned':
                pass
            getattr(model, function)

    def run_simulation(self):
        model = wheel_model.Wheel_model()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Process an exercise according to a given .exc file.')
    parser.add_argument('--file', type=str, default='./exercises/T_pose.exc',
                        help='The name of the file to be simulated (default=%(default)s)')
    parser.add_argument('-t', type=int, default=1, metavar='N',
                        help='amount of times to simulate the current file (default=%(default)d) ')

    args = parser.parse_args()

    simul = Exercise_simulator(args.file, args.t)
