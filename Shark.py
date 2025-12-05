from __future__ import annotations
from Fish import Fish


class Shark( Fish ):
    def __init__(self : Shark, image : str,positionX : int,positionY : int,reproduction_time:int,energy:int ):
        super().__init__(image,positionX,positionY,reproduction_time)
        self.energy = energy
        
    def __repr__(self) -> str:
        return f'Position ({self.positionX}, {self.positionY}) - Temps de reproduction restant "{self.reproduction_time}" chronons - Energie restante "{self.energy}" unités'
    
    def getEnergy(self) -> int:
        return self.energy
    
    def setEnergy(self, energy:int)->bool:
        if energy is None or isinstance(energy, int)==False or energy<0:
            return False
        self.energy = energy
        return True
    
    def decrementEnergy(self)->None:
        self.energy -= 1
        return None
    
    def resetEnergy(self, energy:int)->None:
        self.energy = energy
        return None
    
    def starvation(self)->bool:
        if self.energy <=0:
            self.energy = 0
            return True
        return False
    
if __name__ == "__main__":
    requin = Shark("<img src='shark.png'/>",3,4,5,10)
    print(requin)
    requin.decrementEnergy()
    print(requin)
    requin.resetEnergy(10)
    print(requin)