from __future__ import annotations
from .Fish import Fish


class Shark(Fish):
    """
    A class representing a shark entity in the WA-TOR ecosystem simulation, inheriting from the Fish class.

    Sharks are predators that move, reproduce, and consume fish to survive.
    In addition to the attributes inherited from Fish, sharks have energy and starvation timers.
    A shark dies if it starves (energy reaches zero) and reproduces after a certain number of chronons.

    Attributes:
        reproduction_time (int): Number of chronons required for the shark to reproduce.
        time_left (int): Remaining chronons before the shark can reproduce again.
        image (str): Visual representation or identifier of the shark.
        positionX (int): Current x-coordinate of the shark on the grid.
        positionY (int): Current y-coordinate of the shark on the grid.
        alive (bool): Indicates whether the shark is alive (True) or dead (False).
        energy (int): Current energy level of the shark.
        initial_energy (int): Initial energy level of the shark, used for resetting after feeding.
        starvation_time (int): Number of chronons the shark can survive without eating.
    """

    def __init__(self: Shark, 
                 image: str,
                 positionX: int,
                 positionY: int,
                 reproduction_time: int,
                 starvation_time: int,
                 energy: int):
        super().__init__(image, positionX, positionY, reproduction_time)
        self.energy = energy
        self.initial_energy = energy
        self.starvation_time = starvation_time
        
    def __repr__(self) -> str:
        return (f'Shark at ({self.positionX}, {self.positionY}) - '
                f'Energy: {self.energy}, Time left: {self.time_left}')
    
    def getEnergy(self) -> int:
        return self.energy
    
    # time until shark can live without eating
    def getStarvationTime(self) -> int:
        return self.starvation_time
    
    def setEnergy(self, energy: int) -> bool:
        if energy is None or isinstance(energy, int) == False or energy < 0:
            return False
        self.energy = energy
        return True
    
    def decrementEnergy(self) -> None:
        self.energy -= 1
        if self.isStarving():
            self.die()
    
    def resetEnergy(self) -> None:
        self.energy = self.initial_energy
    
    def isStarving(self) -> bool:
        return self.energy <= 0
    
    def eat(self, fish: Fish, energy_gain: int = 1) -> bool:
        """
        Attempt to eat a fish, increasing the shark's energy if successful.

        The fish is killed, and the shark gains energy if the fish is alive and valid.

        Args:
            fish (Fish): The fish to be eaten.
            energy_gain (int, optional): Amount of energy gained by the shark. Defaults to 1.

        Returns:
            bool: True if the fish was successfully eaten, False otherwise.
        """

        if not isinstance(fish, Fish) or not fish.isAlive():
            return False
        
        fish.die()
        self.energy += energy_gain
        return True
    
    
    def moveTo(self, new_x: int, new_y: int) -> bool:
        """
        Move the shark to a new position on the grid.

        Updates the shark's position, decrements its reproduction timer and energy,
        and checks if the shark is still alive after the move.

        Args:
            new_x (int): The new x-coordinate for the shark.
            new_y (int): The new y-coordinate for the shark.

        Returns:
            bool: True if the shark is still alive after moving, False otherwise.
        """

        if self.setPosition(new_x, new_y):
            self.decrementTimeLeft()
            self.decrementEnergy()
            return self.alive
        return False
    
    def reproduce(self) -> Shark:
        """
        Create a new shark offspring with the same properties as the parent.

        Resets the parent's reproduction timer and returns the new shark instance.

        Returns:
            Shark: A new shark instance with the same attributes as the parent.
        """

        baby = Shark(
            self.image, 
            self.positionX, 
            self.positionY, 
            self.reproduction_time,
            self.starvation_time,
            self.initial_energy
        )
        self.resetTimeLeft()
        return baby


if __name__ == "__main__":
    print("="*50)
    print("SHARK CLASS TESTS")
    print("="*50)
    
    requin = Shark("<img src='shark.png'/>", 3, 4, 12, 6, 10)
    print(f"\n1. Created: {requin}")
    
    requin.decrementEnergy()
    print(f"2. After losing energy: {requin}")
    
    requin.resetEnergy()
    print(f"3. After reset energy: {requin}")
    
    print("\n" + "="*50)
    print("EATING TEST")
    print("="*50)
    
    poisson = Fish("Fish", 5, 5, 8)
    print(f"\nFish before: {poisson} (alive={poisson.isAlive()})")
    print(f"Shark before eating: Energy={requin.getEnergy()}")
    
    requin.eat(poisson)
    
    print(f"\nFish after: {poisson} (alive={poisson.isAlive()})")
    print(f"Shark after eating: Energy={requin.getEnergy()}")
    
    print("\n" + "="*50)
    print("REPRODUCTION TEST")
    print("="*50)
    
    requin.time_left = 0
    
    print(f"\nParent BEFORE reproduction:")
    print(f"   {requin}")
    print(f"   Can reproduce? {requin.canReproduce()}")
    
    if requin.canReproduce():
        baby = requin.reproduce()
        
        print(f"\nBaby created:")
        print(f"   {baby}")
        
        print(f"\nParent AFTER reproduction:")
        print(f"   {requin}")
        
        print(f"\nBaby has {baby.getEnergy()} energy")
        print(f"Parent has {requin.getEnergy()} energy")