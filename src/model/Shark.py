from __future__ import annotations
from model.Fish import Fish


class Shark(Fish):
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
    
    def eat(self, fish: Fish, energy_gain: int = 2) -> bool:
        # Eat a fish and gain energy
        if not isinstance(fish, Fish) or not fish.isAlive():
            return False
        
        fish.die()
        self.energy += energy_gain
        return True
    
    # override methods of fish
    
    def moveTo(self, new_x: int, new_y: int) -> bool:
        # moves like the fish but also loses energy
        if self.setPosition(new_x, new_y):
            self.decrementTimeLeft()
            self.decrementEnergy()
            return self.alive
        return False
    
    def reproduce(self) -> Shark:
        # create a baby shark
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