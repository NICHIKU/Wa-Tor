from __future__ import annotations


class World:
    def __init__(self : World, width : int, height : int, chronons : int = 0):
        self.width = width
        self.height = height
        self.chronons = chronons

        
    def timeFlows(self) -> None:
        self.chronons -= 1
        return None

    
    def getChronons(self) -> int:
        return self.chronons
    
if __name__ == "__main__":
    world = World(10, 10)
    print(f"Chronons: {world.getChronons()}")
    world.timeFlows()
    print(f"Chronons after time flows: {world.getChronons()}")
