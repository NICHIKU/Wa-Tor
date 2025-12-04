from __future__ import annotations
from Fish import Fish
from Shark import Shark

class World:
    def __init__(self : World, width : int, height : int, chronons : int = 0):
        self.width = width
        self.height = height
        self.chronons = chronons
        self.fishes : list[Fish] = []
        self.sharks : list[Shark] = []
        
    def addFish(self, fish : Fish) -> bool:
        if fish is None or not isinstance(fish, Fish):
            return False
        self.fishes.append(fish)
        return True
    
    def addShark(self, shark : Shark) -> bool:
        if shark is None or not isinstance(shark, Shark):
            return False
        self.sharks.append(shark)
        return True
    
    def timeFlows(self) -> None:
        self.chronons += 1
        return None
    
    def getFishes(self) -> list[Fish]:
        return self.fishes
    
    def getSharks(self) -> list[Shark]:
        return self.sharks
    
    def getChronons(self) -> int:
        return self.chronons
    
if __name__ == "__main__":
    world = World(10, 10)
    fish1 = Fish("<img src='fish.png'/>", 2, 3, 5)
    shark1 = Shark("<img src='shark.png'/>", 4, 5, 7, 10)
    
    world.addFish(fish1)
    world.addShark(shark1)
    
    print(f"Chronons: {world.getChronons()}")
    world.timeFlows()
    print(f"Chronons after time flows: {world.getChronons()}")
    print(f"Fishes in the world: {world.getFishes()}")
    print(f"Sharks in the world: {world.getSharks()}")