from __future__ import annotations

class Fish: 
    def __init__(self : Fish, image : str,positionX : int,positionY : int,reproduction_time:int ):
        self.reproduction_time = reproduction_time
        self.image = image
        self.positionX = positionX
        self.positionY = positionY
        
    def __repr__(self) -> str:
        return f'Position ({self.positionX}, {self.positionY}) - Temps de reproduction restant "{self.reproduction_time}" chronons'
    
    def getImage(self) -> str:
        return self.image
    
    def getX(self) -> int:
        return self.positionX
    
    def getY(self) -> int:
        return self.positionY
    
    def getReproduction(self) -> int:
        return self.reproduction_time
    
    def setImage(self, chemin:str)->bool:
        if chemin is None or isinstance(chemin, str)==False:
            return False
        self.image = chemin
        return True
    
    def setX(self, x:int)->bool:
        if x is None or isinstance(x, int)==False or x<0:
            return False
        self.positionX = x
        return True
    
    def setY(self, y:int)->bool:
        if y is None or isinstance(y, int)==False or y<0:
            return False
        self.positionY = y
        return True
    
    def setReproduction(self, reproduction_time:int)->bool:
        if reproduction_time is None or isinstance(reproduction_time, int)==False or reproduction_time<0:
            return False
        self.reproduction_time = reproduction_time
        return True
    
    def decrementReproduction(self)->None:
        self.reproduction_time -= 1
        return None
    
    def resetReproduction(self, reproduction_time:int)->None:
        self.reproduction_time = reproduction_time
        return None
    
if __name__ == "__main__":
    poisson = Fish("<img src='fish.png'/>",5,7,3)
    print(poisson)
    poisson.decrementReproduction()
    print(poisson)
    poisson.resetReproduction(3)
    print(poisson)