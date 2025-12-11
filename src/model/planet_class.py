import numpy as np
import json
from .Fish import Fish
from .Shark import Shark

class WatorPlanet:
    """
    A class representing the WA-TOR ecosystem simulation world (planet).

    This class initializes and manages a grid-based world populated with fish and sharks,
    based on specified percentages. It tracks the population dynamics of both species over time,
    as well as the state of the grid at each chronon (time step).

    Attributes:
        width (int): Width of the simulation grid.
        height (int): Height of the simulation grid.
        perc_fish (float): Percentage of the grid initially populated with fish.
        perc_shark (float): Percentage of the grid initially populated with sharks.
        empty_spaces (int): Number of empty spaces in the grid after initial population.
        chronon (int): Current time step (chronon) of the simulation.
        fishes (list): List of fish entities in the simulation.
        sharks (list): List of shark entities in the simulation.
        fish_population (int): Current number of fish in the simulation.
        shark_population (int): Current number of sharks in the simulation.
        fish_history (list): Historical record of fish population counts over time.
        shark_history (list): Historical record of shark population counts over time.
        grid (2D list): The grid representing the simulation world.
    """

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
            fish = Fish("🐟", int(x), int(y), reproduction_time=2)
            self.fishes.append(fish)
        
        shark_positions = np.argwhere(self.grid == "S")
        for position in shark_positions:
            x, y = position
            shark = Shark("🦈", int(x), int(y), reproduction_time=6, starvation_time=5, energy=2)
            self.sharks.append(shark)
    
    def get_all_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Retrieve the coordinates of all valid neighboring cells around a given position on the grid.

        This method calculates the four orthogonal neighbors (up, down, left, right) of the cell
        at coordinates (x, y), using toroidal (wrapping) boundary conditions. The grid is treated
        as a torus, meaning edges wrap around to the opposite side.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            list[tuple[int, int]]: A list of tuples representing the (x, y) coordinates of neighboring cells.
        """

        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for delta_x, delta_y in directions:
            nx = (x + delta_x) % self.height
            ny = (y + delta_y) % self.width
            neighbors.append((nx, ny))
        return neighbors
    
    def filter_neighbors(self, neighbors: list[tuple[int, int]], content: str) -> list[tuple[int, int]]:
        """
        Filter a list of neighboring coordinates to only include those matching a specific content.

        Args:
            neighbors (list[tuple[int, int]]): List of (x, y) coordinates of neighboring cells.
            content (str): The content to match in the grid (e.g., " ", "F", "S").

        Returns:
            list[tuple[int, int]]: A filtered list of coordinates where the grid content matches the specified value.
        """

        return [(nx, ny) for nx, ny in neighbors if self.grid[nx, ny] == content]
    
    def get_empty_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Retrieve the coordinates of all empty neighboring cells around a given position.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            list[tuple[int, int]]: A list of (x, y) coordinates of empty neighboring cells.
        """

        neighbors = self.get_all_neighbors(x, y)
        return self.filter_neighbors(neighbors, " ")
    
    def get_fish_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Retrieve the coordinates of all neighboring cells containing fish around a given position.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            list[tuple[int, int]]: A list of (x, y) coordinates of neighboring cells containing fish.
        """

        neighbors = self.get_all_neighbors(x, y)
        return self.filter_neighbors(neighbors, "F")
    
    def choose_random_neighbor(self, neighbors: list[tuple[int, int]]) -> tuple[int, int] | None:
        """
        Randomly select a neighbor from a list of coordinates.

        Args:
            neighbors (list[tuple[int, int]]): List of (x, y) coordinates to choose from.

        Returns:
            tuple[int, int] | None: A randomly selected coordinate, or None if the list is empty.
        """

        if len(neighbors) == 0:
            return None
        return neighbors[np.random.randint(len(neighbors))]
    
    def find_fish(self, x: int, y: int) -> Fish | None:
        """
        Find a fish entity at a specific grid position.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            Fish | None: The fish at the specified position, or None if no fish is found or alive.
        """

        for fish in self.fishes:
            if fish.isAlive() and fish.getX() == x and fish.getY() == y:
                return fish
        return None
    
    
    
    def move_fish(self, fish: Fish) -> None:
        """
        Move a fish to a random empty neighboring cell or attempt reproduction if possible.

        If the fish cannot move, its reproduction timer is decremented.
        If the fish can reproduce, a new fish is created and added to the simulation.

        Args:
            fish (Fish): The fish entity to move.
        """

        if not fish.isAlive():
            return
        
        x, y = fish.getPosition()
        empty_neighbors = self.get_empty_neighbors(x, y)
        
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
    
    
    def move_shark(self, shark: Shark) -> None:
        """
        Move a shark according to its behavior: eating, moving, or losing energy if blocked.

        Args:
            shark (Shark): The shark entity to move.
        """

        if not shark.isAlive():
            return
        
        x, y = shark.getPosition()
        
        if self.shark_tries_to_eat(shark, x, y):
            return
        
        if self.shark_tries_to_move(shark, x, y):
            return
        
        self.shark_blocked(shark, x, y)

    def shark_tries_to_eat(self, shark, x, y) -> bool:
        """
        Attempt for a shark to eat a fish in a neighboring cell.

        If successful, the shark's energy is reset, the fish is removed, and the shark moves to the fish's position.

        Args:
            shark (Shark): The shark attempting to eat.
            x (int): The x-coordinate of the shark.
            y (int): The y-coordinate of the shark.

        Returns:
            bool: True if the shark successfully ate a fish, False otherwise.
        """

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
        """
        Attempt for a shark to move to an empty neighboring cell.

        If successful, the shark moves to the new position.

        Args:
            shark (Shark): The shark attempting to move.
            x (int): The x-coordinate of the shark.
            y (int): The y-coordinate of the shark.

        Returns:
            bool: True if the shark successfully moved, False otherwise.
        """

        empty_neighbors = self.get_empty_neighbors(x, y)
        
        if not empty_neighbors:
            return False
        
        new_x, new_y = self.choose_random_neighbor(empty_neighbors)
        self.complete_shark_move(shark, x, y, new_x, new_y)
        return True

    def shark_blocked(self, shark, x, y) -> None:
        """
        Handle the case where a shark cannot move or eat.

        The shark loses energy and dies if its energy reaches zero.

        Args:
            shark (Shark): The shark that is blocked.
            x (int): The x-coordinate of the shark.
            y (int): The y-coordinate of the shark.
        """

        shark.decrementEnergy()
        if not shark.isAlive():
            self.grid[x, y] = " "
            self.shark_population -= 1

    def complete_shark_move(self, shark, x, y, new_x, new_y) -> None:
        """
        Complete the movement of a shark after eating or moving.

        Handles reproduction if possible, updates the grid, and checks if the shark is still alive.

        Args:
            shark (Shark): The shark that moved.
            x (int): The original x-coordinate of the shark.
            y (int): The original y-coordinate of the shark.
            new_x (int): The new x-coordinate of the shark.
            new_y (int): The new y-coordinate of the shark.
        """

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
        """
        Execute a single chronon (time step) of the simulation.

        Shuffles the order of animals, moves each fish and shark, updates populations,
        and increments the chronon counter. Dead animals are removed from the simulation.
        """

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