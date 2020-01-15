import wheel_model
import human_model
import numpy as np


def name_to_function(name, w_model, h_model):
    if name == 'setturned':
        return lambda boolean: (h_model.setturned(bool(boolean)),
                                w_model.set_human_center_of_mass(h_model.getcog()))
    elif name == 'positionchange':
        return lambda *args: (h_model.positionchange(*np.array(args).astype(float)),
                              w_model.set_human_center_of_mass(h_model.getcog()))
    elif name == 'power':
        return lambda place, strength: (w_model.add_force_on_wheel_named(place, float(strength)))


class Exercise_simulator:
    def __init__(self, filename, auto_parse=True):
        self.file = filename
        self.parsed = False
        self.angle_actions = []  # [[angle, f, *args]]
        self.variables = {}
        if auto_parse:
            self.parse()

    def parse(self):
        """Convert the contents of the file given in the init to a list of
        of lists with the inner lists being [angle, f, *args]"""
        with open(self.file, 'r') as f:
            for line in f:
                self.angle_actions.append(line.split())
        self.parsed = True

    def add_custom_variable(self, name, value=0):
        """Adds a custom variable to the simulator; replaces instances of
        name in the exercise files with the given value."""
        self.variables[name] = value

    def setup_angle_actions_model(self, w_model, h_model, auto_parse=True, variables={}):
        """Setup the actual angle actions in the wheel model"""
        if not self.parsed and auto_parse:
            self.parse()
        for angle, function, *args in self.angle_actions:
            for variable, val in self.variables.items():
                args = np.where(np.array(args) == variable,
                                val, np.array(args))
            for variable, val in variables.items():
                print(np.array(args) == variable)
                args = np.where(np.array(args) == variable,
                                val, np.array(args))
            angle = int(angle)
            if angle == 0:
                name_to_function(function, w_model, h_model)(*args)
            else:
                w_model.add_angle_action(
                    angle * np.pi/180, name_to_function(function, w_model, h_model), *args)
        w_model.add_angle_action(2*np.pi, w_model.run_success)

    def run_simulation(self, variables={}):
        w_model = wheel_model.Wheel_model()
        h_model = human_model.human(180, 100, list([0, 0]), 20)
        w_model.set_human_center_of_mass(h_model.getcog())
        self.setup_angle_actions_model(w_model, h_model, variables=variables)
        print(w_model.angle_actions)
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
    simul.run_simulation(variables={'var_power1': 6000, 'var_power2': 3000})
