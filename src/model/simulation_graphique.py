import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import os

CELL_SIZE = 12


class WatorViewer:
    """
    A graphical viewer for the WA-TOR simulation.

    This class provides a Tkinter-based interface to visualize the WA-TOR simulation,
    load simulation data from JSON files, and display population statistics over time.
    It supports playing, pausing, and stepping through the simulation frames.
    """

    def __init__(self, root):
        print(f"Current working dir: {os.getcwd()}")
        self.root = root
        root.title("WA-TOR Graphique Mode")

        self.history = None
        self.fish_history = []
        self.shark_history = []
        self.frame_index = 0
        self.running = False
        self.speed = 150
        self.max_fish = 0
        self.min_fish = 0
        self.max_shark = 0
        self.min_shark = 0

        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack()

        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))     # /wa-Tor/src/model
        SRC_DIR = os.path.dirname(CURRENT_DIR)                       # /wa-Tor/src
        IMG_DIR = os.path.join(SRC_DIR, "img")                       # /wa-Tor/src/img

        fish_path = os.path.join(IMG_DIR, "fish.png")
        shark_path = os.path.join(IMG_DIR, "shark.png")

        if not os.path.exists(fish_path):
            raise FileNotFoundError(f"Image manquante : {fish_path}")

        # Exemple d'utilisation :
        fish_sprite = Image.open(fish_path)
        shark_sprite = Image.open(shark_path)

        ctrl = tk.Frame(root)
        ctrl.pack()

        tk.Button(ctrl, text="📂 Ouvrir JSON", command=self.load_json_dialog).grid(row=0, column=0)
        tk.Button(ctrl, text="▶ Play", command=self.play).grid(row=0, column=1)
        tk.Button(ctrl, text="⏸ Pause", command=self.pause).grid(row=0, column=2)
        tk.Button(ctrl, text="➡ Step", command=self.step).grid(row=0, column=3)

        self.label_frame = tk.Label(ctrl, text="Frame: 0")
        self.label_fish = tk.Label(ctrl, text="Fish: 0")
        self.label_fish.grid(row=0, column=6, padx=10)

        self.label_shark = tk.Label(ctrl, text="Sharks: 0")
        self.label_shark.grid(row=0, column=7, padx=10)

        self.label_frame.grid(row=0, column=4)

        self.speed_scale = tk.Scale(ctrl, from_=30, to=1000,
                                    label="Vitesse (ms)",
                                    orient="horizontal",
                                    command=self.update_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=0, column=5)

        self.sprite_fish = Image.open(fish_path)
        self.sprite_shark = Image.open(shark_path)
        self.sprite_empty = Image.new("RGB", (CELL_SIZE, CELL_SIZE), (0, 0, 40))

        # resized images
        self.sprite_fish = self.sprite_fish.resize((CELL_SIZE, CELL_SIZE))
        self.sprite_shark = self.sprite_shark.resize((CELL_SIZE, CELL_SIZE))
        self.sprite_empty = self.sprite_empty.resize((CELL_SIZE, CELL_SIZE))

        self.sprite_map = {
            "F": self.sprite_fish,
            "S": self.sprite_shark,
            " ": self.sprite_empty
        }

        self.tk_img = None  # prevent garbage collection

    # JSON Gestion

    def load_json_dialog(self):
        """
            Open a file dialog to load a JSON file containing WA-TOR simulation data.
            The loaded data is used to populate the simulation history and initialize the viewer.  
            Args:
                path (str): Path to the JSON file to load.
        """
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DEFAULT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "outputs"))

        path = filedialog.askopenfilename(
            title="Choisir un fichier JSON",
            initialdir=DEFAULT_DIR,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        self.load_json(path)

    def load_json(self, path):
        """
        Load and parse a JSON file containing WA-TOR simulation data.

        This method reads the JSON file, initializes the simulation history, and sets up the viewer
        with the loaded data, including fish and shark population histories.
        It also calculates min/max population values for statistics display.

        Args:
            filepath (str): Path to the JSON file to load.
        """

        print(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.fish_history = []
        self.shark_history = []
        self.frame_index = 0

        # Two possible formats:
        # 1) {"history": [grid0, grid1, ...]} where grid is list of rows
        # 2) {"frames": [{"grid": grid0, "fish": n, "sharks": m}, ...]}
        if "history" in data:
            self.history = np.array(data["history"])
            self.fish_history = [int((frame == "F").sum()) for frame in self.history]
            self.shark_history = [int((frame == "S").sum()) for frame in self.history]
        elif "frames" in data:
            frames = data["frames"]
            grids = []
            for f in frames:
                if "grid" in f:
                    grids.append(f["grid"])
                else:
                    grids.append(f)
                if "fish" in f and "sharks" in f:
                    self.fish_history.append(int(f["fish"]))
                    self.shark_history.append(int(f["sharks"]))
            self.history = np.array(grids)
            if not self.fish_history:
                self.fish_history = [int((frame == "F").sum()) for frame in self.history]
            if not self.shark_history:
                self.shark_history = [int((frame == "S").sum()) for frame in self.history]
    
        self.frames, self.height, self.width = self.history.shape

        if self.fish_history:
            self.min_fish = int(min(self.fish_history))
            self.max_fish = int(max(self.fish_history))
        else:
            self.min_fish = self.max_fish = 0

        if self.shark_history:
            self.min_shark = int(min(self.shark_history))
            self.max_shark = int(max(self.shark_history))
        else:
            self.min_shark = self.max_shark = 0

        # configure canvas
        self.canvas.config(width=self.width * CELL_SIZE,
                           height=self.height * CELL_SIZE)

        self.frame_index = 0
        self.draw_frame(0)

        print(f"OK JSON chargé ({self.width}×{self.height}) — {self.frames} Chronons")
        print(f"Fish history (sample): {self.fish_history[:5]} ...")
        print(f"Shark history (sample): {self.shark_history[:5]} ...")
        print(f"Fish min/max: {self.min_fish}/{self.max_fish}")
        print(f"Shark min/max: {self.min_shark}/{self.max_shark}")

        print(f"OK JSON chargé ({self.width}×{self.height}) — {self.frames} Chronons")


    def draw_frame(self, idx):
        """
        Draw the current simulation frame on the canvas.
        It uses the preloaded sprites to represent fish, sharks, and empty cells.
        The technique involves creating a full PIL image for efficiency, then converting it to a Tkinter image for display.

        Args:
            frame_index (int): The index of the frame to draw.
        """

        if self.history is None:
            return
        if self.frame_index == (self.frames-1):
            self.running = False
            self.open_stats_window()
        grid = self.history[idx]

        self.update_population_labels(grid)
        frame_img = Image.new("RGB", (self.width * CELL_SIZE, self.height * CELL_SIZE))

        for y in range(self.height):
            for x in range(self.width):
                tile = self.sprite_map.get(grid[y][x], self.sprite_empty)
                frame_img.paste(tile, (x * CELL_SIZE, y * CELL_SIZE))

        self.tk_img = ImageTk.PhotoImage(frame_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        self.label_frame.config(text=f"Chronons: {idx}/{self.frames-1}")



    def update_speed(self, v):
        """
        Update the playback speed of the simulation.

        This method adjusts the delay between frames during playback.

        Args:
            speed (int): New speed value in milliseconds.
        """

        self.speed = int(v)

    def play(self):
        """
        Start or resume the simulation playback.

        This method sets the simulation to running and begins the update loop.
        """

        if not self.running:
            self.running = True
            self.update_loop()

    def pause(self):
        """
        Pause the simulation playback.

        This method stops the update loop, freezing the simulation at the current frame.
        """

        self.running = False

    def step(self):
        """
        Advance the simulation by one frame.

        This method increments the frame index and redraws the grid for the new frame.
        """

        self.pause()
        if self.history is None:
            return
        self.frame_index = (self.frame_index + 1) % self.frames
        self.draw_frame(self.frame_index)

    def update_loop(self):
        """
        Update the simulation frame in a loop while the simulation is running.

        This method advances the frame index, redraws the current frame, and schedules the next update.
        If the simulation is paused or no history is loaded, the loop stops.
        """

        if not self.running or self.history is None:
            return
        self.frame_index = (self.frame_index + 1) % self.frames
        self.draw_frame(self.frame_index)
        self.root.after(self.speed, self.update_loop)

    def update_population_labels(self, grid):
        """
        Update the labels displaying the current fish and shark populations.

        Counts the number of fish ("F") and sharks ("S") in the current grid and updates the corresponding labels.

        Args:
            grid (numpy.ndarray): The current state of the simulation grid.
        """

        fish_count = np.count_nonzero(grid == "F")
        shark_count = np.count_nonzero(grid == "S")

        self.label_fish.config(text=f"Fish: {fish_count}")
        self.label_shark.config(text=f"Sharks: {shark_count}")

        
    def open_stats_window(self):
        """
        Open a new window displaying population statistics and a plot of fish and shark populations over time.

        This window shows the maximum and minimum populations of fish and sharks,
        the total number of chronons, and a plot of population trends using Matplotlib.
        The plot is embedded in the window using a Tkinter canvas.
        """

        win = tk.Toplevel(self.root)
        win.title("Population Stats")
        win.geometry("600x500")  # plus grand pour accueillir le graphique

        # === FRAME DES STATS TEXTUELLES ===
        stats_frame = tk.Frame(win)
        stats_frame.pack(side="top", fill="x", pady=10)

        tk.Label(stats_frame, text=f"🐟 Fish max : {self.max_fish}").pack(anchor="w", padx=10)
        tk.Label(stats_frame, text=f"🐟 Fish min : {self.min_fish}").pack(anchor="w", padx=10)
        tk.Label(stats_frame, text=f"🦈 Shark max : {self.max_shark}").pack(anchor="w", padx=10)
        tk.Label(stats_frame, text=f"🦈 Shark min : {self.min_shark}").pack(anchor="w", padx=10)

        tk.Label(stats_frame, text=f"Chronons : {len(self.fish_history)-1}").pack(anchor="w", padx=10)

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)

        ax.plot(self.fish_history, label="Fish", color="blue")
        ax.plot(self.shark_history, label="Sharks", color="red")

        ax.set_title("Population Fish Time")
        ax.set_xlabel("Chronons")
        ax.set_ylabel("Population")
        ax.grid(True)
        ax.legend()

        # Canvas Tkinter
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


        


if __name__ == "__main__":
    root = tk.Tk()
    viewer = WatorViewer(root)
    root.mainloop()