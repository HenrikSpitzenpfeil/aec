import os
import json

from secm import SECM
from Experiments import AbstractExperiment, LineSweep, NovaProcedure
from autolab import Potentiostat
from aec.config.definitions import ROOT_DIR

"""TODO: Make Experiment loading more universal so that code doesn't need to be changed """

def main():
  secm = SECM()
  with open(os.path.join(ROOT_DIR, "config\\autolab_config.json")) as config: # Access and load config file
    autolab_config  = json.load(config)
  potentiostat = Potentiostat(config = autolab_config)
    # TODO: Implement Experiment configs

  #Prompt user to insert experiment settings path
  experiment_path = input_experiment()

  with open(experiment_path) as config:
    experiment_config = json.load(config)
    experiment_class = experiment_config["experiment_class"]
    experiment_metadata = experiment_config["experiments_metadata"]
    experiment_settings = experiment_config["experiment_settings"]

  number_of_experiments = int(input('Please input Number of Experiments to perform'))
  
  secm.new_substrate()
    
  while True:
    for experiment in range(number_of_experiments):
      experiment.measure(experiment_config)
      experiment.save_data(save_path)
      secm.prepare_next_experiment(config["spot_increment"])

def input_experiment() -> os.PathLike:

  """Prompt user to input the path to the Experiment file to be executed"""

  experiment_path = input("Please input absolute path to experiment json file")
  experiment_path = os.path.normpath(experiment_path)
  if os.path.exists(experiment_path):
    pass
  else:
    print("Input path does not exist")
    return input_experiment()
  
  if os.path.isfile(experiment_path):
    return(experiment_path)
  else:
    print("Input path is not a file")
    return input_experiment()