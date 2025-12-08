import numpy as np

class wator_planet:
    
    def __init__(self,
                 width: int,
                 height: int,
                 perc_fish: float, #it's here mainly for test
                 perc_shark: float, #it's here mainly for test
                 fish_reproduction_time: int = 8,
                 shark_reproduction_time: int = 12,
                 shark_starvation_time: int = 5,
                 shark_initial_energy: int = 5
                 ):
        self.width = width
        self.height = height
        self.perc_fish = perc_fish
        self.perc_shark = perc_shark
        """ Put x and y on the fish and shark class to retrieve them for the rest of the code """
        """ This atributes could also go to fish and shark. Create an animal class? """
        self.fish_reproduction_time = fish_reproduction_time
        self.shark_reproduction_time = shark_reproduction_time
        self.shark_starvation_time = shark_starvation_time
        self.shark_initial_energy = shark_initial_energy
        
        world_spaces = height * width
        self.fish_population = int(perc_fish * world_spaces)
        self.shark_population = int(perc_shark * world_spaces)
        self.empty_spaces = world_spaces - self.fish_population - self.shark_population
        
        self.chronon = 0
        """ the births and energy should go to fish and shark 
        Maybe find an intersection between fish and shark as a "animal_birth" or something like that """
        self.fish_time_left = {}
        self.shark_time_left = {}
        self.shark_energy = {} 
        self.create_grid()
        
        self.fish_history = [self.fish_population]
        self.shark_history = [self.shark_population]
    
    def create_grid(self): #stays
        #Create initial grid with fish, sharks, and empty spaces
        array = np.concatenate([
            np.full(self.fish_population, "F"),
            np.full(self.shark_population, "S"),
            np.full(self.empty_spaces, " ")])

        np.random.shuffle(array)
        self.grid = array.reshape(self.height, self.width)
        
        self.initialize_population()
    

    def initialize_population(self):
        fish_positions = np.argwhere(self.grid == "F")
        for position in fish_positions:
            x, y = position
            self.fish_time_left[(x, y)] = self.fish_reproduction_time
        shark_positions = np.argwhere(self.grid == "S")
        for position in shark_positions:
            x, y = position
            self.shark_time_left[(x, y)] = self.shark_reproduction_time
            self.shark_energy[(x, y)] = self.shark_initial_energy

    def movement_result(self):
        #Move all animals once per turn
        filled_animal = np.argwhere(self.grid != " ")
        # who moves first is random at every turn
        np.random.shuffle(filled_animal)
        
        for position in filled_animal:
            x, y = position
            self.animal_movement(x, y)
        
        self.chronon += 1
        self.fish_history.append(self.fish_population)
        self.shark_history.append(self.shark_population)
    
    
    def get_random_neighbor(self, x, y):
        #Get random neighboring position with toroidal wrap
        direction = np.random.choice(["up", "down", "right", "left"])
        movements = {
            "up": (-1, 0),
            "down": (1, 0),
            "right": (0, 1),
            "left": (0, -1)
        }
        
        delta_x, delta_y = movements[direction]
        new_x = (x + delta_x) % self.height
        new_y = (y + delta_y) % self.width
        
        return new_x, new_y
    
    #code a modifier avec les methodes de classe
    '''
    def get_age_and_position(self):
        
    '''
    """ This two can become just one as well """
    """ def get_fish_age(self, x, y):
        #Calculate age of fish at position x, y
        birth_time = self.fish_birth.get((x, y), 0)
        return self.chronon - birth_time
    
    def get_shark_age(self, x, y):
        #Calculate age of shark at position x, y
        birth_time = self.shark_birth.get((x, y), 0)
        return self.chronon - birth_time"""
    
    # Fish functions
    
    def move_fish(self, x, y, new_x, new_y):
        # Move fish with reproduction logic
        self.fish_time_left[(x, y)] -= 1
        
        if self.fish_time_left[(x, y)]  <= 0:
            self.reproduce_fish(x, y, new_x, new_y)
        else:
            self.move_fish_only(x, y, new_x, new_y)
    
    def reproduce_fish(self, x, y, new_x, new_y):
        #Fish reproduces: baby stays at old position, adult moves
        # Baby fish stays
        self.grid[x, y] = "F"
        self.fish_time_left[(x, y)] = self.fish_reproduction_time
        self.fish_population += 1
        
        # Adult fish moves
        self.grid[new_x, new_y] = "F"
        self.fish_time_left[(new_x, new_y)] = self.fish_reproduction_time
    
    def move_fish_only(self, x, y, new_x, new_y):
        #Fish just moves without reproducing        

        self.grid[new_x, new_y] = "F"
        self.fish_time_left[(new_x, new_y)] = self.fish_time_left[(x,y)]
        if (x, y) in self.fish_time_left:
            del self.fish_time_left[(x,y)]
        
        self.grid[x, y] = " "
    
    # Shark functions
    
    def move_shark(self, x, y, new_x, new_y, current_energy):
        #Move shark with eating and reproduction logic
        self.shark_time_left[(x, y)] -= 1
        
        # Check if shark eats fish
        if self.grid[new_x, new_y] == "F":
            current_energy = self.shark_eats_fish(new_x, new_y, current_energy)
        
        # Shark survives: move or reproduce
        if self.shark_time_left[(x, y)]  <= 0:
            self.reproduce_shark(x, y, new_x, new_y, current_energy)
        else:
            self.move_shark_only(x, y, new_x, new_y, current_energy)
    
    def shark_eats_fish(self, new_x, new_y, current_energy):
        #Shark eats fish at new position
        self.fish_population -= 1
        current_energy += 2  # Gain energy from eating
        
        if (new_x, new_y) in self.shark_time_left:
            del self.shark_time_left[(new_x, new_y)]
        
        return current_energy
    
    def shark_dies(self, x, y):
        #Shark dies because it did not eat
        self.grid[x, y] = " "
        self.shark_population -= 1
        
        if (x, y) in self.shark_time_left:
            del self.shark_time_left[(x, y)]
        if (x, y) in self.shark_energy:
            del self.shark_energy[(x, y)]
    
    def reproduce_shark(self, x, y, new_x, new_y, current_energy):
        #Shark reproduces: baby stays at old position, adult moves
        # Baby shark
        self.grid[x, y] = "S"
        self.shark_time_left[(x, y)] = self.shark_starvation_time
        self.shark_energy[(x, y)] = self.shark_initial_energy
        self.shark_population += 1
        
        # Adult shark
        self.grid[new_x, new_y] = "S"
        self.shark_time_left[(new_x, new_y)] = self.shark_starvation_time
        self.shark_energy[(new_x, new_y)] = current_energy
    
    def move_shark_only(self, x, y, new_x, new_y, current_energy):
        #Shark just moves without reproducing
        
        self.grid[new_x, new_y] = "S"
        self.shark_time_left[(new_x, new_y)] = self.shark_time_left[(x,y)]
        
        self.grid[x, y] = " "
        
        if (x, y) in self.shark_time_left:
            del self.shark_time_left[(x,y)]
        if (x, y) in self.shark_energy:
            del self.shark_energy[(x, y)]
        
        self.grid[x, y] = " "
    
    def get_neighbour_list(self,x,y, new_x, new_y, current_energy):
        #get a list of neighbours so the shark searches the fishes
        neighbours = []
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        for delta_x, delta_y in directions:  
                nx = (x + delta_x) % self.height
                ny = (y + delta_y) % self.width
                neighbours.append((nx, ny))
             
        for neighbour in neighbours:
            if self.grid[neighbour[0], neighbour[1]] == "F":
                self.move_shark(x, y, neighbour[0], neighbour[1], current_energy)
                break
                     
        else:
            if self.grid[new_x, new_y] != "S":
                self.move_shark(x, y, new_x, new_y, current_energy)
                    
    def animal_movement(self, x, y):
        #Coordinate movement of animal at position x,y
        if self.grid[x, y] == " ":
            return
        
        animal_type = self.grid[x, y]
        new_x, new_y = self.get_random_neighbor(x, y)
        
        if animal_type == "F":
            if self.grid[new_x, new_y] == " ":
                self.move_fish(x, y, new_x, new_y)
        
        elif animal_type == "S":
            # Shark loses energy each turn
            current_energy = self.shark_energy.get((x, y), self.shark_initial_energy)
            current_energy -= 1
            
            # Check if shark lost all its energy
            if current_energy <= 0:
                self.shark_dies(x, y)
                return
            
            self.shark_energy[(x, y)] = current_energy
            
            self.get_neighbour_list(x,y,new_x,new_y, current_energy)
                    
                     
def simulation(num_chronons):
    
    planet = wator_planet(
        width=10,
        height=10,
        perc_fish=0.01,
        perc_shark=0.01,
        fish_reproduction_time=8,
        shark_reproduction_time=12,
        shark_starvation_time=5,
        shark_initial_energy=5
    )
    
    print("Initial grid:")
    print(planet.grid)
    print(f"Fish: {planet.fish_population} | Sharks: {planet.shark_population}")
    print(f"Chronon: {planet.chronon}\n")
    
    for i in range(num_chronons):
        planet.movement_result()
        
        print("=" * 50)
        print(f"Chronon {planet.chronon}:")
        print(planet.grid)
        print(f"Fish: {planet.fish_population} | Sharks: {planet.shark_population}")
       
    
    print("Simulation complete!")
    return planet


# Test
if __name__ == "__main__":
    simulation(20)
