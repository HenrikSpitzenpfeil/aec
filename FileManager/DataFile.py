from FileManager import FileManager
from dataclasses import dataclass, field
from datetime import datetime
import os
import csv
import pandas as pd

@dataclass
class SECMDataFile:

    """ Dataclass for an SECM experiment
    containing the dataset aswell as the metadata for it."""

    file_path: os.PathLike
    data: pd.DataFrame
    experiment_name: str
    experiment_id: str
    substrate_material: str
    batch_id: int 
    ai_model: str = None
    ai_model_id: str = None
    coordinates: list[float] = field(default_factory=list)
    date: str = str(datetime.now().replace(microsecond=0))
    

    def write_to_csv(self) -> None:

        """ Writes the data to a CSV file at the specified file path."""

        if os.path.isfile(self.file_path): #Check if the file already exists so not to overwrite existing data
            print ("File already exists")
            return
        
        with open(self.file_path, 'w',newline='') as csv_file:
            writer = csv.writer(csv_file) # Write the CSV file header

            writer.writerow(("Experiment Name", self.experiment_name))
            writer.writerow(("Experiment Id", self.experiment_id))
            writer.writerow(("Substrate Material", self.substrate_material))
            writer.writerow(("Batch Id", self.batch_id))
            writer.writerow(("Ai Model", self.ai_model))
            writer.writerow(("Ai Model Id", self.ai_model_id))
            writer.writerow(("Substrate Coordinates", self.coordinates))
            writer.writerow(("Date", self.date))
            writer.writerow(())

        self.data.to_csv(self.file_path,
                         sep = ",",
                         mode = "a",
                         header = True) #appends the data to the CSV file.

def parse_secm_datafile(file_path) -> SECMDataFile:

    """Reads the SECM Data into a SECMDataFile object."""

    with open(file_path, 'r', newline= '') as csv_file:
        reader = csv.reader(csv_file)

        attributes = []
        for line in reader: #collects alls attributes from the csv file in a list
            if line == []:
                break
            attributes.append(line[1])
    #TODO: Remove the magic number somehow
    dataframe = pd.read_csv(file_path, sep = ',', skiprows= 9) # get the data from the file to a dataframe
    
    return SECMDataFile(file_path, dataframe, *attributes)