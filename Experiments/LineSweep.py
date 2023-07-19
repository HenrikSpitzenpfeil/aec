from Experiments.AbstractExperiment import AbstractExperiment
from autolab import Potentiostat
import time
import os
import pandas as pd

class LineSweep(AbstractExperiment):

    """ Experiment Class to perform a line sweep experiment
    using a autolab potentiostat.
    
    The measure method performs the experiment.
    Data is stored in the results_data attribute as a pandas dataframe.
    The save_data method saves the data as a csv file to the provided location """

    def __init__ (self, potentiostat: Potentiostat):
        
        self.potentiostat = potentiostat
        self.results_data = pd.DataFrame(columns= ["time",
                                                   "potential",
                                                   "current",
                                                   "potential_applied"])

    def measure(self,
                start_potential: float,
                end_potential: float,
                scan_rate: float,
                step_potential: float) -> None:
        
        step_interval = step_potential/scan_rate
        potential_to_apply = start_potential
        time_list = []
        potential_list = []
        current_list = []
        potential_applied_list = []
        start_time = time.time()

        if not self.results_data.empty: # empty results data frame if there is data from a previous measurement
            self.results_data.drop(self.results_data.index, inplace= True)

        for step in range(round((end_potential- start_potential)/step_interval)):
            
            self.potentiostat.set_potential(potential_to_apply)
            res_potential, res_current, res_applied_potential = self.potentiostat.get_actual_values()

            time_list.append(time.time() - start_time)
            potential_list.append(res_potential)
            current_list.append(res_current)
            potential_applied_list.append(res_applied_potential)

            potential_to_apply += step_potential
            time.sleep(step_interval)
  
        self.results_data["time"] = time_list
        self.results_data["potential"] = potential_list
        self.results_data["current"] = current_list
        self.results_data["potential_applied"] = potential_applied_list
    
    def save_data(self, save_path: os.PathLike) -> None:

        self.results_data.to_csv(save_path, sep = ",")        