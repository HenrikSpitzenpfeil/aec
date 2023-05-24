import secm
from Experiments import Experiments
from autolab import autolab

'TODO: Implement everything'

def main():
    #microscope = secm.SECM(self, config, config, Electrode, substrate)
    #experiment = Experiments.DummyExperiment(self, microscope)
    number_of_experiments = int(input('Please insert Number of Experiments to perform'))
    experiments_performed = 0
    
    while True:
        if experiments_performed == number_of_experiments:
          break
        # elif secm.spots_left == 0:
        #   secm.new_substrate()
        # else:
            # experiment.measure
            # secm.next_spot
            #experiments_performed += 1