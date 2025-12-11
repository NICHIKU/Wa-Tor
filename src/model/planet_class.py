import numpy as np
import json
from Fish import Fish
from Shark import Shark

class WatorPlanet:
    
    def __init__(self,
                 width: int,
                 height: int,
                 perc_fish: float,
                 perc_shark: float):
        
        self.width = width
        self.height = height
        self.perc_fish = perc_fish
        self.perc_shark = perc_shark
        
        world_spaces = height * width
        initial_fish_count = int(perc_fish * world_spaces)
        initial_shark_count = int(perc_shark * world_spaces)
        self.empty_spaces = world_spaces - initial_fish_count - initial_shark_count
        
        self.chronon = 0
        
        self.fishes = []
        self.sharks = []
        
        self.fish_population = initial_fish_count
        self.shark_population = initial_shark_count
        
        self.create_grid()
        
        self.fish_history = [self.fish_population]
        self.shark_history = [self.shark_population]
    
    def create_grid(self):
        array = np.concatenate([
            np.full(self.fish_population, "F"),
            np.full(self.shark_population, "S"),
            np.full(self.empty_spaces, " ")
        ])
        
        np.random.shuffle(array)
        self.grid = array.reshape(self.height, self.width)
        
        self.initialize_population()
    
    def initialize_population(self):
        fish_positions = np.argwhere(self.grid == "F")
        for position in fish_positions:
            x, y = position
            fish = Fish("🐟", int(x), int(y), reproduction_time=8)
            self.fishes.append(fish)
        
        shark_positions = np.argwhere(self.grid == "S")
        for position in shark_positions:
            x, y = position
            shark = Shark("🦈", int(x), int(y), reproduction_time=12, starvation_time=5, energy=4)
            self.sharks.append(shark)
    
    def get_all_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for delta_x, delta_y in directions:
            nx = int((x + delta_x)) % self.height
            ny = int((y + delta_y)) % self.width
            neighbors.append((nx, ny))
        return neighbors
    
    def filter_neighbors(self, neighbors: list[tuple[int, int]], content: str) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in neighbors if self.grid[nx, ny] == content]
    
    def get_empty_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = self.get_all_neighbors(x, y)
        return self.filter_neighbors(neighbors, " ")
    
    def get_fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors = self.get_all_neighbors(x, y)
        return self.filter_neighbors(neighbors, "F")
    
    def choose_random_neighbor(self, neighbors: list[tuple[int, int]]) -> tuple[int, int] | None:
        if len(neighbors) == 0:
            return None
        return neighbors[np.random.randint(len(neighbors))]
    
    def find_fish(self, x: int, y: int) -> Fish | None:
        # method t help the shark to find the fish
        for fish in self.fishes:
            if fish.isAlive() and fish.getX() == x and fish.getY() == y:
                return fish
        return None
    
    # fish movement functions
    
    def move_fish(self, fish: Fish) -> None:
        if not fish.isAlive():
            return
        
        x, y = fish.getPosition()
        empty_neighbors = self.get_empty_neighbors(x, y)
        
        # If no empty space, stay in place
        if not empty_neighbors:
            fish.decrementTimeLeft()
            return
        new_x, new_y = self.choose_random_neighbor(empty_neighbors)
        
        if fish.canReproduce():
            baby = fish.reproduce()
            self.fishes.append(baby)
            self.grid[x, y] = "F"
            self.fish_population += 1
        else:
            self.grid[x, y] = " "
    
        fish.moveTo(new_x, new_y)
        self.grid[new_x, new_y] = "F"
    
    # shark movement functions
    
    def move_shark(self, shark: Shark) -> None:
        if not shark.isAlive():
            return
        
        x, y = shark.getPosition()
        
        if self.shark_tries_to_eat(shark, x, y):
            return
        
        if self.shark_tries_to_move(shark, x, y):
            return
        
        self.shark_blocked(shark, x, y)

    def shark_tries_to_eat(self, shark, x, y) -> bool:
        fish_neighbors = self.get_fish_neighbors(x, y)
        
        if not fish_neighbors:
            return False
        
        target_x, target_y = self.choose_random_neighbor(fish_neighbors)
        target_fish = self.find_fish(target_x, target_y)
        
        if not target_fish or not target_fish.isAlive():
            return False
        
        shark.eat(target_fish)
        self.fish_population -= 1
        
        self.complete_shark_move(shark, x, y, target_x, target_y)
        return True

    def shark_tries_to_move(self, shark, x, y) -> bool:
        empty_neighbors = self.get_empty_neighbors(x, y)
        
        if not empty_neighbors:
            return False
        
        new_x, new_y = self.choose_random_neighbor(empty_neighbors)
        self.complete_shark_move(shark, x, y, new_x, new_y)
        return True

    def shark_blocked(self, shark, x, y) -> None:
        shark.decrementEnergy()
        if not shark.isAlive():
            self.grid[x, y] = " "
            self.shark_population -= 1

    def complete_shark_move(self, shark, x, y, new_x, new_y) -> None:
        if shark.canReproduce():
            baby = shark.reproduce()
            self.sharks.append(baby)
            self.grid[x, y] = "S"
            self.shark_population += 1
        else:
            self.grid[x, y] = " "
        
        shark.moveTo(new_x, new_y)
        
        if not shark.isAlive():
            self.grid[new_x, new_y] = " "
            self.shark_population -= 1
        else:
            self.grid[new_x, new_y] = "S"
                        
    def movement_result(self) -> None:
        all_animals = self.fishes + self.sharks
        np.random.shuffle(all_animals)
        
        for animal in all_animals:
            if not animal.isAlive():
                continue
            
            if isinstance(animal, Shark):
                self.move_shark(animal)
            elif isinstance(animal, Fish):
                self.move_fish(animal)
                
        self.fishes = [fish for fish in self.fishes if fish.isAlive()]
        self.sharks = [shark for shark in self.sharks if shark.isAlive()]

        self.chronon += 1
        self.fish_history.append(self.fish_population)
        self.shark_history.append(self.shark_population)

def simulation(num_chronons: int):
    world = WatorPlanet(
        width=10,
        height=10,
        perc_fish=0.01,
        perc_shark=0.01
    )
    
    print("=" * 50)
    print("WA-TOR SIMULATION")
    print("=" * 50)
    print("Initial grid:")
    print(world.grid)
    print(f"Fish: {world.fish_population} | Sharks: {world.shark_population}")
    print(f"Chronon: {world.chronon}\n")
    
    for i in range(num_chronons):
        world.movement_result()
        
        print("=" * 50)
        print(f"Chronon {world.chronon}:")
        print(world.grid)
        print(f"Fish: {world.fish_population} | Sharks: {world.shark_population}")
    print("\nSimulation complete!")
    return world


if __name__ == "__main__":
    simulation(10)