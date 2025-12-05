from Fish import Fish
from Shark import Shark
from World import World

world = World(5, 5)

default_fish_image = "<img src='fish.png'/>"
default_fish_reproduction_time = 3

default_shark_image = "<img src='shark.png'/>"
default_shark_reproduction_time = 5
default_shark_energy = 10

def initialize_simulation() -> list:
    grid = [[None] * world.width for _ in range(world.height)] 
    fish1 = Fish(default_fish_image, 4, 4, default_fish_reproduction_time)
    shark1 = Shark(default_shark_image, 1, 1, default_shark_reproduction_time, default_shark_energy)
    grid[fish1.getY()][fish1.getX()] = fish1
    grid[shark1.getY()][shark1.getX()] = shark1
    
    return grid

def move_entity(entity, new_x: int, new_y: int, grid: list) -> bool:
    if (0 <= new_x < world.width) and (0 <= new_y < world.height):
        grid[entity.getY()][entity.getX()] = None
        entity.setX(new_x)
        entity.setY(new_y)
        grid[new_y][new_x] = entity
        return True
    return False

def print_grid(grid: list) -> None:
    for row in grid:
        row_repr = ""
        for cell in row:
            if cell is None:
                row_repr += "[   ] "
            elif isinstance(cell, Fish):
                if isinstance(cell, Shark):
                    row_repr += "[ S ] "
                else:
                    row_repr += "[ F ] "
            elif isinstance(cell, Shark):
                row_repr += "[ S ] "
        print(row_repr)
        
def auto_move_entities(grid: list) -> None:
    for y in range(world.height):
        for x in range(world.width):
            entity = grid[y][x]
            if entity is not None:
                new_x = (x + 1) % world.width
                new_y = y
                move_entity(entity, new_x, new_y, grid)
                
if __name__ == "__main__":
    simulation_grid = initialize_simulation()
    print("Initial Grid:")
    print_grid(simulation_grid)
    
    auto_move_entities(simulation_grid)
    print("\nGrid after moving entities:")
    print_grid(simulation_grid)