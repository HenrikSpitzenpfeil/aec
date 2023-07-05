from AbstractExperiment import AbstractExperiment
from autolab.autolab import potentiostat
import os
import time

class NovaProcedure(AbstractExperiment):

    def __init__(self,
                 procedure_path: os.PathLike,
                 potenstiostat: potentiostat):

        self.potentiostat = potenstiostat
        self.procedure = self.potentiostat.instrument.LoadProcedure(procedure_path)
    
    def measure(self) -> None:
        self.procedure.Measure()
        while self.procedure.IsMeasuring():
            time.sleep(0.1)

    def save_data(self, save_path: os.PathLike) -> None:
        self.procedure.SaveAs(save_path)