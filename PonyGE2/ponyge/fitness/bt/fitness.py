from ponyge.fitness.base_ff_classes.base_ff import base_ff



class fitness(base_ff):
    maximise = True  # True as it ever was.
    def __init__(self, parameter):
        # Initialise base fitness function class.
        super().__init__()
        self.parameter = parameter
        self.fit_func = parameter.params['BTSETTINGS'].bt_fitness

    def evaluate(self, ind, **kwargs):
        # ind.phenotype will be a xml file. We can parse through the xml file
        # and determine the diversity based on the nodes
        return self.fit_func(ind, self.parameter)
