from Experiments.AbstractExperiment import AbstractExperiment
from autolab.autolab import Potentiostat
import os
import time

class NovaProcedure(AbstractExperiment):

    def __init__(self,
                 procedure_path: os.PathLike,
                 potenstiostat: Potentiostat):

        self.potentiostat = potenstiostat
        self.procedure = self.potentiostat.instrument.LoadProcedure(procedure_path)
        self.file_type = ".nox"
    
    def measure(self) -> None:

        """ Measures the Objects loaded .nox procedure"""

        self.procedure.Measure()
        while self.procedure.IsMeasuring:
            time.sleep(0.1)

    def save_data(self, save_path: os.PathLike) -> None:
        
        """ Saves the .nox procedure to given file path"""
        self.procedure.SaveAs(save_path)