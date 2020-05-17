from abc import abstractmethod

class BaseModule:
    
    @property
    @abstractmethod
    def variable_name(self):
        pass

    @abstractmethod
    def step(self, timestep):
        pass
    
    @abstractmethod
    def reset(self):
        pass

    