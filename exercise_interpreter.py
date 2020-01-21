import wheel_model
import human_model
import numpy as np


def name_to_function(name, w_model, h_model):
    """ Interpret the key words in the excercise files into functions."""
    if name == 'setturned':
        return lambda boolean: (h_model.setturned(bool(boolean)),
                                w_model.set_human(h_model))
    elif name == 'positionchange':
        return lambda *args: (h_model.positionchange(*np.array(args).astype(float)),
                              w_model.set_human(h_model))
    elif name == 'power':
        return lambda place, strength: (w_model.add_force_on_wheel_named(place, float(strength)))
    elif name == 'remove_all_forces':
        return w_model.remove_all_forces


class Exercise_simulator:
    def __init__(self, filename, iterations, simul_time=20.0, auto_parse=True, visual=False):
        self.file = filename
        self.iterations = iterations
        self.parsed = False
        # [[angle, f, *args]]
        self.angle_actions = []
        self.variables = {}
        self.simul_time = simul_time
        self.visual = visual
        if auto_parse:
            self.parse()

    def parse(self):
        """ Convert the contents of the file given in the init to a list of
            of lists with the inner lists being [angle, f, *args]"""
        with open(self.file, 'r') as f:
            for line in f:
                self.angle_actions.append(line.split())

        self.parsed = True

    def add_custom_variable(self, name, value=0):
        """ Adds a custom variable to the simulator; replaces instances of
            name in the exercise files with the given value."""
        self.variables[name] = value

    def setup_angle_actions_model(self, w_model, h_model, auto_parse=True, variables={}):
        """ Setup the actual angle actions in the wheel model"""
        if not self.parsed and auto_parse:
            self.parse()

        for angle, function, *args in self.angle_actions:
            for variable, val in {**self.variables, **variables}.items():
                args = np.where(np.array(args) == variable,
                                val, np.array(args))
                args = np.where(np.array(args) == '-' + variable,
                                -val, np.array(args))
            angle = int(angle)

            if angle == 0:
                name_to_function(function, w_model, h_model)(*args)
            else:
                w_model.add_angle_action(
                    angle * np.pi/180, name_to_function(function, w_model, h_model), *args)

        w_model.add_angle_action(2*np.pi, w_model.run_success)

    def run_simulation(self, variables={}, visual=False):
        """ Run the simulation with the correct variables and actions."""
        w_model = wheel_model.Wheel_model(visual=(visual or self.visual))
        h_model = human_model.human(160, 55, list([0, 0]), 42)
        w_model.set_human(h_model)
        self.setup_angle_actions_model(w_model, h_model, variables=variables)

        res = w_model.run(max_run_time=self.simul_time)
        return res
