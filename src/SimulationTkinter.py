import tkinter as tk
from Fish import Fish
from Shark import Shark
from Simulation import initialize_simulation, move_entity
from World import World
import random
CELL_SIZE = 80

class SimulationTkinter:
    def __init__(self, root, world: World, grid: initialize_simulation):
        self.world = world
        self.grid = grid
        self.root = root
        

        self.canvas = tk.Canvas(root,
                                width=world.width * CELL_SIZE,
                                height=world.height * CELL_SIZE,
                                bg="white")
        self.canvas.pack()

        self.create_grid()

        self.fish = world.fishes[0]

        self.img = tk.PhotoImage(file = self.fish.image)
        self.canvas_img_id = None
        

        self.create_fish()

        self.move_after_tkinter()

    def create_grid(self):
        for y in range(self.world.height):
            for x in range(self.world.width):
                self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    outline="gray"
                )

    def create_fish(self):
        x = self.fish.getX() * CELL_SIZE + CELL_SIZE // 2
        y = self.fish.getY() * CELL_SIZE + CELL_SIZE // 2

        if self.canvas_img_id is None:
            self.canvas_img_id = self.canvas.create_image(x, y, image=self.img)
        else:
            self.canvas.coords(self.canvas_img_id, x, y)

    def move_after_tkinter(self):
        self.root.after(5000, self.move_entity_random)

    def move_entity_random(self):
        x = self.fish.getX()
        y = self.fish.getY()
        moves = []

        # gestion des bordures
        
        moves.append(((x - 1) % world.width, y))
        moves.append(((x + 1) % world.width, y))
        moves.append((x, (y - 1) % world.height))
        moves.append((x, (y + 1) % world.height))

        if moves:
            new_x, new_y = random.choice(moves)
            move_entity(self.fish, new_x, new_y, self.grid)

        self.create_fish()
        self.move_after_tkinter()

if __name__ == "__main__":
    world = World(5,5)
    fish1 = Fish("fish.png", 2, 3, 5)
    
    world.addFish(fish1)
    simulation_grid = initialize_simulation()

    root = tk.Tk()
    SimulationTkinter(root, world, simulation_grid)

    root.mainloop()
