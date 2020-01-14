import wheel_model
import human_model
import numpy as np

def name_to_function(name, w_model, h_model):
    if name == 'setturned':
        return  lambda boolean: (h_model.setturned(bool(boolean)), w_model.set_human_center_of_mass(h_model.getcog()))
    elif name == 'positionchange':
        return lambda *args: (h_model.positionchange(*np.array(args).astype(float)), w_model.set_human_center_of_mass(h_model.getcog()))
    elif name == 'power':
        return lambda *args: (w_model.add_force_on_wheel_named(args[0], float(args[1])))

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

    def setup_angle_actions_model(self, w_model, h_model):
        for angle, function, *args in self.angle_actions:
            if angle == 0:
                name_to_function(function, w_model, h_model)(*args)
            else:
                w_model.add_angle_action(int(angle) * np.pi/180, name_to_function(function, w_model, h_model), *args)
        w_model.add_angle_action(2*np.pi, w_model.run_success)

    def run_simulation(self):
        w_model = wheel_model.Wheel_model()
        h_model = human_model.human(180,100,list([0,0]),20)
        w_model.set_human_center_of_mass(h_model.getcog())
        self.setup_angle_actions_model(w_model, h_model)
        print(w_model.run())


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
    simul.run_simulation()
