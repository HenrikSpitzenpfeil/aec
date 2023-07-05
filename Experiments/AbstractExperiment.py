import abc
from abc import ABC


class AbstractExperiment(ABC):

    @abc.abstractmethod
    def __init__(self):
        ...
    
    @abc.abstractmethod
    def measure(self):
        ...
    
    @abc.abstractmethod
    def save_data(self):
        ...