from __future__ import annotations

class Fish: 
    """
    A class representing a fish entity in the WA-TOR ecosystem simulation.

    Fish are characterized by their position on a grid, a visual representation,
    and a reproduction timer. Each fish moves, reproduces, and interacts with its environment
    based on the simulation rules.

    Attributes:
        reproduction_time (int): Number of chronons required for the fish to reproduce.
        time_left (int): Remaining chronons before the fish can reproduce again.
        image (str): Visual representation or identifier of the fish.
        positionX (int): Current x-coordinate of the fish on the grid.
        positionY (int): Current y-coordinate of the fish on the grid.
        alive (bool): Indicates whether the fish is alive (True) or dead (False).
    """

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
    
    def getPosition(self) -> tuple[int, int]:
        return (self.positionX, self.positionY)
    
    def getReproduction(self) -> int:
        return self.reproduction_time
    
    def getTimeLeft(self) -> int:
        return self.time_left
    
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
    
    def setPosition(self, x: int, y: int) -> bool:
        return self.setX(x) and self.setY(y)
    
    def setReproduction(self, reproduction_time: int) -> bool:
        if reproduction_time is None or isinstance(reproduction_time, int) == False or reproduction_time < 0:
            return False
        self.reproduction_time = reproduction_time
        return True
    
    # ===== REPRODUCTION METHODS =====
    
    def decrementTimeLeft(self) -> None:
        if self.time_left > 0:
            self.time_left -= 1
    
    def resetTimeLeft(self) -> None:
        self.time_left = self.reproduction_time
    
    def canReproduce(self) -> bool:
        return self.time_left <= 0
    
    def reproduce(self) -> Fish:
        """
        Create a new fish offspring with the same properties as the parent.

        This method generates a new fish at the parent's current position,
        resets the parent's reproduction timer, and returns the new fish instance.

        Returns:
            Fish: A new fish instance with the same image and reproduction time as the parent.
        """

        baby = Fish(self.image, self.positionX, self.positionY, self.reproduction_time)
        self.resetTimeLeft()
        return baby
    
    
    def moveTo(self, new_x: int, new_y: int) -> bool:
        """
        Move the fish to a new position on the grid.

        This method attempts to update the fish's position to the specified coordinates.
        If the move is successful, the fish's reproduction timer is decremented.

        Args:
            new_x (int): The new x-coordinate for the fish.
            new_y (int): The new y-coordinate for the fish.

        Returns:
            bool: True if the move was successful, False otherwise.
        """

        if self.setPosition(new_x, new_y):
            self.decrementTimeLeft()
            return True
        return False
    
    def die(self) -> None:
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