import numpy as np
import json
from Fish import Fish
from Shark import Shark
from typing import Dict, List

class wator_planet:
    
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
        
        # Lists of Fish and Shark objects
        self.fishes = []
        self.sharks = []
        
        self.fish_population = initial_fish_count
        self.shark_population = initial_shark_count
        
        self.create_grid()
        
        self.fish_history = [self.fish_population]
        self.shark_history = [self.shark_population]
    
    def create_grid(self):
        #Create initial grid with fish, sharks, and empty spaces
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
            shark = Shark("🦈", int(x), int(y), reproduction_time=12, starvation_time=5, energy=10)
            self.sharks.append(shark)
    
    def get_all_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        #Get all 4 neighboring positions with toroidal wrap
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for delta_x, delta_y in directions:
            nx = int((x + delta_x)) % self.height
            ny = int((y + delta_y)) % self.width
            neighbors.append((nx, ny))
        return neighbors
    
    def filter_neighbors(self, neighbors: list[tuple[int, int]], content: str) -> list[tuple[int, int]]:
        # Filter neighbors by grid content
        return [(nx, ny) for nx, ny in neighbors if self.grid[nx, ny] == content]
    
    def get_empty_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        # Get all empty neighboring positions
        neighbors = self.get_all_neighbors(x, y)
        return self.filter_neighbors(neighbors, " ")
    
    def get_fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        # Get all neighboring positions with fish
        neighbors = self.get_all_neighbors(x, y)
        return self.filter_neighbors(neighbors, "F")
    
    def choose_random_neighbor(self, neighbors: list[tuple[int, int]]) -> tuple[int, int] | None:
        # chose a random neighbour from the list, if there is any it returns None
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
        # fish must be alive to move
        if not fish.isAlive():
            return
        
        x, y = fish.getPosition()
        #print(f"Fish before: ({x}, {y})") 
        # Get empty neighbors
        empty_neighbors = self.get_empty_neighbors(x, y)
        
        # If no empty space, stay in place
        if not empty_neighbors:
            fish.decrementTimeLeft()
            return
        
        # Choose random empty neighbor
        new_x, new_y = self.choose_random_neighbor(empty_neighbors)
        
        # Check reproduction
        if fish.canReproduce():
            baby = fish.reproduce()
            self.fishes.append(baby)
            self.grid[x, y] = "F"
            self.fish_population += 1
        else:
            self.grid[x, y] = " "
        
        # Move fish
        fish.moveTo(new_x, new_y)
        #print(f"Fish after: {fish.getPosition()}") 
        self.grid[new_x, new_y] = "F"
    
    # shark movement functions
    
    def move_shark(self, shark: Shark) -> None:
        # Check if shark is still alive
        if not shark.isAlive():
            return
        
        x, y = shark.getPosition()
        
        # Look for fish in neighbors
        fish_neighbors = self.get_fish_neighbors(x, y)

        # Tries to eat a fish
        if fish_neighbors:
            # Choose a random fish neighbor
            target_x, target_y = self.choose_random_neighbor(fish_neighbors)
            
            # Find and eat the fish
            target_fish = self.find_fish(target_x, target_y)
            
            # Check if the fish is alive and valid
            if target_fish and target_fish.isAlive():
                shark.eat(target_fish)
                self.fish_population -= 1
                new_x, new_y = target_x, target_y
                
                # The moving shark goes to the fish's position, leaves empty behind and maybe baby
                #moved_to_empty = False
            else:
                # The found fish is not alive/valid, so try to move to an empty space
                empty_neighbors = self.get_empty_neighbors(x, y)
                if not empty_neighbors:
                    # Blocked, only lose energy (might starve)
                    shark.decrementEnergy()
                    if not shark.isAlive():
                        self.grid[x, y] = " "
                        self.shark_population -= 1
                    return
                # Move to empty space and lose energy
                new_x, new_y = self.choose_random_neighbor(empty_neighbors)
                #moved_to_empty = True
                
        # If no fish found, try to move to an empty space
        else:
            empty_neighbors = self.get_empty_neighbors(x, y)
            
            if not empty_neighbors:
                # Blocked - lose energy and stay in place (might starve)
                shark.decrementEnergy()
                if not shark.isAlive():
                    self.grid[x, y] = " "
                    self.shark_population -= 1
                return
            
            # Move to empty space and lose energy
            new_x, new_y = self.choose_random_neighbor(empty_neighbors)
           # moved_to_empty = True
        
        # Reproduction occurs before the shark moves
        if shark.canReproduce():
            baby = shark.reproduce()
            self.sharks.append(baby)
            self.grid[x, y] = "S"  # Baby stays at the old position
            self.shark_population += 1
        else:
            self.grid[x, y] = " "
        
        # Move the shark to the new position
        shark.moveTo(new_x, new_y)
        
        # If the shark died from starvation during moveTo
        if not shark.isAlive():
            self.grid[new_x, new_y] = " "
            self.shark_population -= 1
        else:
            self.grid[new_x, new_y] = "S"
            
        # Energy and reproduction time decrement is already handled in shark.moveTo()
                        
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



def export_to_json(world, filename: str = "simulation_data.json") -> None:
    """
    Exporte les données de simulation dans un fichier JSON.
    
    Args:
        world: Instance de wator_planet contenant les données de simulation
        filename: Nom du fichier JSON à créer (par défaut: "simulation_data.json")
    """
    data = {
        "simulation_parameters": {
            "width": world.width,
            "height": world.height,
            "initial_fish_percentage": world.perc_fish,
            "initial_shark_percentage": world.perc_shark
        },
        "chronons": []
    }
    
    for chronon in range(len(world.fish_history)):
        data["chronons"].append({
            "chronon": chronon,
            "fish_count": world.fish_history[chronon],
            "shark_count": world.shark_history[chronon]
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Données exportées dans '{filename}'")
    print(f"  - Nombre de chronons: {len(world.fish_history)}")
    print(f"  - Population finale - Poissons: {world.fish_population}, Requins: {world.shark_population}")


def export_to_json_compact(world, filename: str = "simulation_data_compact.json") -> None:
    """
    Version compacte : exporte uniquement les listes de populations.
    
    Args:
        world: Instance de wator_planet
        filename: Nom du fichier JSON
    """
    data = {
        "fish_population": world.fish_history,
        "shark_population": world.shark_history
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Données compactes exportées dans '{filename}'")

def simulation(num_chronons: int):
    world = wator_planet(
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
        export_to_json(world)
        print("=" * 50)
        print(f"Chronon {world.chronon}:")
        print(world.grid)
        print(f"Fish: {world.fish_population} | Sharks: {world.shark_population}")
    print("\nSimulation complete!")
    return world


if __name__ == "__main__":
    simulation(10)