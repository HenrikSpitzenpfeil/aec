import abc
from abc import ABC

class AbstractAi(ABC):

    @abc.abstractmethod
    def __init__(self):
        ...
    
    @abc.abstractmethod
    def get_decision(self):
        ...
    