from model.Fish import Fish
from model.Shark import Shark
from model.World import World
from random import randrange

witdh = 5
height = 5
chronons = 20

nb_sharks = 2
nb_fish = 10

world = World(witdh, height, chronons)

default_fish_image = "<img src='img/fish.png'/>"
default_fish_reproduction_time = 5

default_shark_image = "<img src='img/shark.png'/>"
default_shark_reproduction_time = 12
default_shark_energy = 5

def initialize_simulation(nb_sharks :int, nb_fish:int) -> list:
    grid = [[None] * world.width for _ in range(world.height)] 
    
    for x in range(nb_fish):
        while True:
            posX = randrange(0, world.width)
            posY = randrange(0, world.height)
            if grid[posY][posX] is None:
                fish = Fish(default_fish_image, posX, posY, default_fish_reproduction_time)
                grid[posY][posX] = fish
                break
    
    for x in range(nb_sharks):
        while True:
            posX = randrange(0, world.width)
            posY = randrange(0, world.height)
            if grid[posY][posX] is None:
                shark = Shark(default_shark_image, posX, posY, default_shark_reproduction_time, default_shark_energy)
                grid[posY][posX] = shark
                break
    
    return grid

def move_entity(entity, new_x: int, new_y: int, grid: list) -> bool:
    target_cell = grid[new_y][new_x]
    
    if isinstance(entity, Shark):
        entity.decrementEnergy()
        if entity.starvation():
            print(f"💀 Un requin est mort de faim en ({entity.getX()}, {entity.getY()}) !")
            grid[entity.getY()][entity.getX()] = None 
            return True

    if target_cell is None:
        grid[entity.getY()][entity.getX()] = None 
        entity.setX(new_x)
        entity.setY(new_y)
        grid[new_y][new_x] = entity 
        return True

    elif isinstance(entity, Shark) and isinstance(target_cell, Fish) and not isinstance(target_cell, Shark):
        print(f"⚔️ Un requin a mangé un poisson en ({new_x}, {new_y}) !")
        entity.resetEnergy(default_shark_energy)  
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
        print(row_repr)
        
def auto_move_entities(grid: list) -> None:
    moved_entities = set()
    
    for y in range(world.height):
        for x in range(world.width):
            entity = grid[y][x]
            if entity is not None and entity not in moved_entities:
                value = randrange(1, 3)      
                if value == 1:
                    move_val = randrange(-1, 2, 2) 
                    new_x = (x + move_val) % world.width
                    new_y = y
                elif value == 2:
                    move_val = randrange(-1, 2, 2)
                    new_x = x
                    new_y = (y + move_val) % world.height     
                move_entity(entity, new_x, new_y, grid)
                moved_entities.add(entity)
                reproduce_entities(entity, grid, x, y)

                
def reproduce_entities(entity, grid : list, x: int, y: int) -> None:
    if grid[y][x] is None:
        if isinstance(entity, Shark):
            if entity.getReproduction() > 0:
                entity.decrementReproduction()
                return None
            else:
                new_shark = Shark(default_shark_image, x, y, default_shark_reproduction_time, default_shark_energy)
                grid[y][x] = new_shark
        elif isinstance(entity, Fish) and not isinstance(entity, Shark):
            if entity.getReproduction() > 0:
                entity.decrementReproduction()
                return None
            else:
                new_fish = Fish(default_fish_image, x, y, default_fish_reproduction_time)
                grid[y][x] = new_fish

def check_habitat(grid:list) ->str:
    sharks = 0
    fish = 0  
    for x in range(world.width):
        for y in range(world.height):
            entity = grid[y][x]
            if isinstance(entity, Shark):
                sharks += 1
            elif isinstance(entity, Fish) and not isinstance(entity, Shark):
                fish += 1
    return f"Habitat has {sharks} sharks and {fish} fish"
        
                
if __name__ == "__main__":
    simulation_grid = initialize_simulation(nb_sharks, nb_fish)
    
    while world.getChronons() > 0:
        print_grid(simulation_grid)
        auto_move_entities(simulation_grid)
        print("\n")
        world.timeFlows()
    print("Simulation ended.")
    print(check_habitat(simulation_grid))