import numpy as np
import time
import os
import pandas as pd


from .utils import current_density
from gym.core import Env
from gym import spaces
from autolab import Potentiostat
from secm import SECM
from math import pi

class OerEnvironment (Env):

    """An Open Ai Gym environment for the Sensolytics SECM
      and a Metrohm Autolab Potentiostat"""

    def __init__(self, potentiostat: Potentiostat, secm: SECM) -> None:
        
        #TODO: how to check if potentiostat is connected
        self.potentiostat = potentiostat
        self.secm = secm
        
        #Distance between experiment spots on the substrate surface
        self.distance_between_spots = 2500
        
        #Maximum number of steps in an epsiode
        self.max_episode_length = 1500
        
        # Starting potential to be applied at the beginning of an epsiode
        self.start_potential = 0 #V
        # Rate at which the potential can be changed by the agent
        self.scan_rate = 0.005 #V/s
        # Change of potential for each step
        self.potential_step = 0.00244 #V
        # Time to wait between each step
        self.wait_time = self.potential_step/self.scan_rate
        
        self.episode_length = 0
        self.state = self.start_potential
        self.action_space = spaces.Discrete(n = 3)
        self.observation_space = spaces.Box(low = np.array([0, -0.03, -0.1]), high = np.array([0.65, np.inf, 0.7]))
        self.spec = None

        self.overpotential_procedure = "Overpotential.nox"


    def step(self, action: int) -> tuple:
        # Action = 2 increase the Applied potential by potential step
        if action == 2:
            self.state += self.potential_step
        # Action = 1 decrease the applied potential by potential step
        elif action == 1:
            self.state -= self.potential_step
        # Otherwise stay on current potential
        else:
            pass
        #Increment episode length
        self.episode_length += 1
        #Set state as potential 
        self.potentiostat.set_potential(self.state)
        #Wait for until next step can be executed
        time.sleep(self.wait_time)

        if self.episode_length >= self.max_episode_length:
            overpotential = self.measure_overpotential(self.overpotential_procedure)
            reward = self.reward_function(target, overpotential)
            done = True
        else: 
            done = False
            reward = 0
        
        #Get the state of the experiment from the potentiostat
        observation = np.asarray(self.potentiostat.get_actual_values())
        
        # Placeholder for info
        info = {}

        return observation, reward, done, info

    def reset(self) -> None:
        self.secm.move_to_next_experiment(self.distance_between_spots)
        self.state = self.start_potential
        self.episode_length = 0
    
    def close(self):
        """Closes the environment and resets the SECM position to wash."""
        self.secm.move_to_wash()
        #TODO: shut off and disconnect potentiostat

    def reward_function(self, target_overpotential: float,
                        observed_overpotential: float) -> float:
        
        """Calculates the reward for an observed overpotential and a given target overpotential.
        Reward is normalized to the target overpotential."""

        return (target_overpotential-observed_overpotential)/target_overpotential

    def measure_overpotential(self, procedure_path) -> float:
        
        """Uses a predefined nova procedure to measure a linear sweep.
        Interpolates the overpotential at 0.01 A/cm^-2 by linear interpolation.
        This method has to many responsibilities should probably be split up."""

        def overpotential(polyfit: np.array) -> float:
            return (0.01-polyfit[1])/polyfit[0]

        #Load the procedure to measure Overpotential
        procedure = self.potentiostat.instrument.LoadProcedure(procedure_path)
        #Measure the procedure
        procedure.Measure()
        while procedure.IsMeasuring:
            time.sleep(0.1)
        df = pd.DataFrame()    
        
        #Grab the data from the measured procedure
        command = procedure.Commands["CV staircase"]
        for column in command.Signals.Names:
            if len(list(command.Signals.get_Item(column).Value)) != 0:
                df[column] = list(command.Signals.get_Item(column).Value)
        # Calculate the current density from the data
        df["current density"] = df["WE(1).Current"].map(current_density)
        df = df.loc[df['Scan'] == 1]
        
        #linear interpolation of the values around the overpotential at 0.01 A/cm-2
        line_fit_table = df.loc[(df["current density"]> 0.008) & (df["current density"] < 0.015) & (df["Index"] < 250)]
        line_fit = np.polyfit(line_fit_table["Potential applied"], line_fit_table["current density"], 1)
        return overpotential(line_fit)
    
class OerEnvironmentSim (Env):

    def __init__(self, potentiostat: Potentiostat, secm: SECM) -> None:
        
        #TODO: how to check if potentiostat is connected
        self.potentiostat = potentiostat
        self.secm = secm
        
        #Distance between experiment spots on the substrate surface
        self.distance_between_spots = 2500
        
        #Maximum number of steps in an epsiode
        self.max_episode_length = 10
        
        # Starting potential to be applied at the beginning of an epsiode
        self.start_potential = 0 #V
        # Rate at which the potential can be changed by the agent
        self.scan_rate = 0.005 #V/s
        # Change of potential for each step
        self.potential_step = 0.00244 #V
        # Time to wait between each step
        self.wait_time = self.potential_step/self.scan_rate
        
        self.episode_length = 0
        #TODO: should probably rename this attribute
        self.state = self.start_potential
        self.action_space = spaces.Discrete(n = 3)
        self.observation_space = spaces.Box(low = np.array([0, -0.03, -0.1]), high = np.array([0.65, np.inf, 0.7]))
        self.spec = None

        self.overpotential_procedure = "Overpotential.nox"


    def step(self, action: int) -> tuple:
        # Action = 2 increase the Applied potential by potential step
        if action == 2:
            self.state += self.potential_step
        # Action = 1 decrease the applied potential by potential step
        elif action == 1:
            self.state -= self.potential_step
        # Otherwise stay on current potential
        else:
            pass
        #Increment episode length
        self.episode_length += 1
        #Set state as potential 
        self.potentiostat.set_potential(self.state)
        #Wait for until next step can be executed
        time.sleep(self.wait_time)

        if self.episode_length >= self.max_episode_length:
            print("measuring overpotential")
            reward = 1
            done = True
        else: 
            done = False
            reward = 0
        
        #Get the state of the experiment from the potentiostat
        observation = self._get_obs()
        
        # Placeholder for info
        info = {}

        return observation, reward, done, info

    def reset(self) -> tuple:
    #TODO: Implement this correctly according to open ai gym specifications
        print("reseting the environment")
        self.state = self.start_potential
        self.episode_length = 0
        self.potentiostat.set_potential(self.state)
        info = {}
        return self._get_obs(), info
    
    def close(self):
        print("closing environment, moving to wash position")
        #TODO: shut off and disconnect potentiostat

    # def reward_function(self, target_overpotential: float, observed_overpotential: float) -> float:
    #     """Calculates the reward for an observed overpotential and a given target overpotential.
    #     Reward is normalized to the target overpotential."""
    #     return (target_overpotential-observed_overpotential)/target_overpotential

    # def measure_overpotential(self, procedure_path) -> float:
        
    #     def overpotential(polyfit: np.array) -> float:
    #         return (0.01-polyfit[1])/polyfit[0]

    #     #Load the procedure to measure Overpotential
    #     procedure = self.potentiostat.instrument.LoadProcedure(procedure_path)
    #     #Measure the procedure
    #     procedure.Measure()
    #     while procedure.IsMeasuring:
    #         time.sleep(0.1)
    #     df = pd.DataFrame()    
        
    #     #Grab the data from the measured procedure
    #     command = procedure.Commands["CV staircase"]
    #     for column in command.Signals.Names:
    #         if len(list(command.Signals.get_Item(column).Value)) != 0:
    #             df[column] = list(command.Signals.get_Item(column).Value)
    #     # Calculate the current density from the data
    #     df["current density"] = df["WE(1).Current"].map(current_density)
    #     df = df.loc[df['Scan'] == 1]
        
    #     #linear interpolation of the values around the overpotential at 0.01 A/cm-2
    #     line_fit_table = df.loc[(df["current density"]> 0.008) & (df["current density"] < 0.015) & (df["Index"] < 250)]
    #     line_fit = np.polyfit(line_fit_table["Potential applied"], line_fit_table["current density"], 1)
    #     return overpotential(line_fit)
    
    def _get_obs(self) -> tuple:
        return np.asarray(self.potentiostat.get_actual_values())