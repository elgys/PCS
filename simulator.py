import wheel_model
import human_model
import numpy as np


def name_to_function(name, w_model, h_model):
    """ Interpret the key words in the excercise files into functions."""
    if name == 'setturned':
        return lambda boolean: (h_model.setturned(boolean == 'True'))
    elif name == 'positionchange':
        return lambda *args: (h_model.positionchange(*np.array(args).astype(float)),
                              w_model.set_human(h_model))
    elif name == 'power':
        return lambda place, strength: (w_model.add_force_on_wheel_named(place, float(strength)))
    elif name == 'remove_all_forces':
        return w_model.remove_all_forces


class simulator:
    """ This class combines two models into a simulation."""
    def __init__(self, filename, simul_time=20.0,
                 length = 160, weight = 55, auto_parse=True, variables = {}):
        self.file = filename
        self.lenght = 160
        self.weight = 55
        self.parsed = False
        self.angle_actions = []
        self.variables = variables
        self.simul_time = simul_time
        self.w_model = wheel_model.Wheel_model(self.simul_time)
        self.h_model = human_model.human(self.lenght, self.weight, list([0, 0]), 42)
        self.w_model.set_human(self.h_model)

        if auto_parse:
            self.parse()
            self.setup_angle_actions_model(self.w_model, self.variables)

    def parse(self):
        """ Convert the contents of the file given in the init to a list of
            of lists with the inner lists being [angle, f, *args]."""
        with open(self.file, 'r') as f:
            for line in f:
                self.angle_actions.append(line.split())

        self.parsed = True

    def add_custom_variable(self, name, value=0):
        """ Adds a custom variable to the simulator; replaces instances of
            name in the exercise files with the given value."""
        self.variables[name] = value

    def setup_angle_actions_model(self, auto_parse=True, variables={},
                                  force=25000):
        """ Setup the actual angle actions in the wheel model."""
        if not self.parsed and auto_parse:
            self.parse()

        for angle, function,*args in self.angle_actions:
            args = self.variable_calc(variables, args, force)

            for variable, val in {**self.variables, **variables}.items():
                args = np.where(np.array(args) == variable,
                                val, np.array(args))
                args = np.where(np.array(args) == '-' + variable,
                                -val, np.array(args))

            angle = int(angle)

            if angle == 0:
                name_to_function(function, self.w_model, self.h_model)(*args)
            else:
                self.w_model.add_angle_action(angle * np.pi / 180,
                                         name_to_function(function, self.w_model,
                                         self.h_model), *args)

        self.w_model.add_angle_action(2 * np.pi, self.w_model.run_success)

    def variable_calc(self, variables, args, force):
        """ Looks for the difference between variables and strings."""
        new = []

        for arg in args:
            if arg[0] is '"' and arg[-1] is '"':
                new.append(arg[1:-1])
            elif arg.isnumeric():
                new.append(float(arg))
            elif arg not in self.variables and arg[1:] not in self.variables:
                new.append(arg)

                if arg[0] == '-':
                    arg = arg[1:]

                self.variables[arg] = force
            else:
                new.append(arg)

        return new

    def step(self):
        """ Takes step in the simulation."""
        return self.w_model.step()

    def reset(self, variables={}):
        """ Reset the simulation."""
        self.parsed = False
        self.angle_actions = []
        self.variables = variables
        self.w_model = wheel_model.Wheel_model(self.simul_time)
        self.h_model = human_model.human(self.lenght, self.weight, list([0, 0]), 42)
        self.w_model.set_human(self.h_model)
        self.parse()
        self.setup_angle_actions_model(self.w_model)

    def get_results(self):
        """ Get the results from the simulation."""
        return self.w_model.get_max_angle()

    def run_simulation(self, variables={}, visual=False):
        """ Run the simulation with the correct variables and actions."""
        res = self.w_model.run(max_run_time=self.simul_time, visual=visual)

        return res
