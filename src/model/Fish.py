from __future__ import annotations

class Fish: 
    def __init__(self: Fish, 
                 image: str,
                 positionX: int,
                 positionY: int,
                 reproduction_time: int):
        self.reproduction_time = reproduction_time
        self.time_left = reproduction_time
        self.image = image
        self.positionX = positionX
        self.positionY = positionY
        self.alive = True
        
    def __repr__(self) -> str:
        return f'Fish at ({self.positionX}, {self.positionY}) - Time left: {self.time_left}'
    
    def getImage(self) -> str:
        return self.image
    
    def getX(self) -> int:
        return self.positionX
    
    def getY(self) -> int:
        return self.positionY
    
    #easier to use inside the world code
    def getPosition(self) -> tuple[int, int]:
        return (self.positionX, self.positionY)
    
    def getReproduction(self) -> int:
        return self.reproduction_time
    
    def getTimeLeft(self) -> int:
        # time left until reproduction
        return self.time_left
    
    # check if animal is dead to continue the interaction
    def isAlive(self) -> bool:
        return self.alive
    
    def setImage(self, chemin: str) -> bool:
        if chemin is None or isinstance(chemin, str) == False:
            return False
        self.image = chemin
        return True
    
    def setX(self, x: int) -> bool:
        if x is None or isinstance(x, int) == False or x < 0:
            return False
        self.positionX = x
        return True
    
    def setY(self, y: int) -> bool:
        if y is None or isinstance(y, int) == False or y < 0:
            return False
        self.positionY = y
        return True
    
    #same as previously
    def setPosition(self, x: int, y: int) -> bool:
        return self.setX(x) and self.setY(y)
    
    def setReproduction(self, reproduction_time: int) -> bool:
        if reproduction_time is None or isinstance(reproduction_time, int) == False or reproduction_time < 0:
            return False
        self.reproduction_time = reproduction_time
        return True
    
    # ===== REPRODUCTION METHODS =====
    
    def decrementTimeLeft(self) -> None:
        #Decrement time left until reproduction
        if self.time_left > 0:
            self.time_left -= 1
    
    def resetTimeLeft(self) -> None:
        #Reset time left to base reproduction time
        self.time_left = self.reproduction_time
    
    def canReproduce(self) -> bool:
        #Check if fish can reproduce
        return self.time_left <= 0
    
    def reproduce(self) -> Fish:
        #Create a baby fish at current position
        baby = Fish(self.image, self.positionX, self.positionY, self.reproduction_time)
        self.resetTimeLeft()
        return baby
    
    # movement methods
    
    def moveTo(self, new_x: int, new_y: int) -> bool:
        #Move to new position and decrement time left
        if self.setPosition(new_x, new_y):
            self.decrementTimeLeft()
            return True
        return False
    
    # life status 
    def die(self) -> None:
        # Mark fish as dead
        self.alive = False


if __name__ == "__main__":
    poisson = Fish("<img src='fish.png'/>", 5, 7, 3)
    print(poisson)
    poisson.decrementTimeLeft()
    print(poisson)
    poisson.resetTimeLeft()
    print(poisson)
    
    # Test methods
    print(f"\nPosition: {poisson.getPosition()}")
    print(f"Time left: {poisson.getTimeLeft()}")
    print(f"Can reproduce? {poisson.canReproduce()}")
    
    # Test reproduction
    poisson.time_left = 0
    if poisson.canReproduce():
        print(f"\nParent before reproduction: {poisson}")
        baby = poisson.reproduce()
        print(f"Baby fish: {baby}")
        print(f"Parent after reproduction: {poisson}")