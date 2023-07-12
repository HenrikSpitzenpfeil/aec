from secm import SECM
from Experiments import AbstractExperiment, LineSweep, NovaProcedure
from autolab import Potentiostat

"""TODO: Make Experiment loading more universal so that code doesn't need to be changed """

def main():
    secm = SECM()
    potentiostat = Potentiostat(config = config)
    experiment = LineSweep.LineSweep(potentiostat)
    # TODO: Implement Experiment configs
    number_of_experiments = int(input('Please input Number of Experiments to perform'))
    secm.new_substrate()
    
    while True:
        for experiment in range(number_of_experiments):
          experiment.measure(experiment_config)
          experiment.save_data(save_path)
          secm.prepare_next_experiment(config["spot_increment"])
        