import os 

class FileManager:

    """ FileManager class responsible for finding and creating directories,
      filenames and paths where experimental data is stored. 
      Encapsulates the logic for a simple folder structure.
      
    Folder Structure that this FileManager creates:
      Save Data
        Experiment Name
            batchid_experimentnumber_ experimentname.csv
        AI Experiment
           AI Model
              batchid_experimentnumber_ experimentname.csv """

    def __init__(self, root_save_path: os.PathLike):
        self.root_path = root_save_path
    
    def generate_file_name(self,
                           batch_id: int,
                           experiment_number: int,
                           experiment_name: str) -> str:
        
        """ Generates the file name for an experiment from the experiment name
          the experiment number in the current batch and the batch id."""
        
        return "{:03d}".format(batch_id)+ "_" + "{:03d}".format(experiment_number)+ "_" + experiment_name +".csv"
    
    def generate_folder_path(self,
                           experiment_name: str,
                           ai_model_name: str = None) -> str:
        
        """Returns the folder path from root save path and experiment name.
        If it is an Ai experiment and an Ai model name is specified a sub directory
        of the experiment name is added to the folder path."""

        if ai_model_name is not None:
           return  os.path.join(self.root_path,
                                experiment_name,
                                ai_model_name)
        else:
            return os.path.join(self.root_path, experiment_name)

    def check_create_folder(self, folder_path) -> str:
        
        """Check if the given path is a directory. 
        If it does not exist it creates the folder.
        Returns a human readable string, spefifying 
        if the folder exists or was created"""

        if os.path.exists(folder_path): # checks if directory exists
            return "folder exists" # directory exists already therefore exit the method
        
        else:
            os.makedirs(folder_path) # create directory at given path
            return "folder was created"
    
