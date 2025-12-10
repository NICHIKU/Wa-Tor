import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import os

CELL_SIZE = 8


class WatorViewerFast:
    def __init__(self, root):
        print(f"Current working dir: {os.getcwd()}")
        self.root = root
        root.title("WA-TOR Graphique Mode")

        self.history = None
        self.frame_index = 0
        self.running = False
        self.speed = 150

        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack()

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

        self.sprite_fish = Image.open("fish.png")
        self.sprite_shark = Image.open('shark.png')
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
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.load_json(path)

    def load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.history = np.array(data["history"])
        self.frames, self.height, self.width = self.history.shape

        self.canvas.config(width=self.width * CELL_SIZE,
                           height=self.height * CELL_SIZE)

        self.frame_index = 0
        self.draw_frame(0)

        print(f"OK JSON chargé ({self.width}×{self.height}) — {self.frames} Chronons")

    # Grid creation

    def draw_frame(self, idx):
        if self.history is None:
            return

        grid = self.history[idx]

        self.update_population_labels(grid)

        # Create a full PIL image (fast & memory-efficient)
        frame_img = Image.new("RGB", (self.width * CELL_SIZE, self.height * CELL_SIZE))

        for y in range(self.height):
            for x in range(self.width):
                tile = self.sprite_map.get(grid[y][x], self.sprite_empty)
                frame_img.paste(tile, (x * CELL_SIZE, y * CELL_SIZE))

        # Convert to Tk image
        self.tk_img = ImageTk.PhotoImage(frame_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        self.label_frame.config(text=f"Chronons: {idx}/{self.frames-1}")

    # function 

    def update_speed(self, v):
        self.speed = int(v)

    def play(self):
        if not self.running:
            self.running = True
            self.update_loop()

    def pause(self):
        self.running = False

    def step(self):
        self.pause()
        if self.history is None:
            return
        self.frame_index = (self.frame_index + 1) % self.frames
        self.draw_frame(self.frame_index)

    def update_loop(self):
        if not self.running or self.history is None:
            return
        self.frame_index = (self.frame_index + 1) % self.frames
        self.draw_frame(self.frame_index)
        self.root.after(self.speed, self.update_loop)

    def update_population_labels(self, grid):
        fish_count = np.count_nonzero(grid == "F")
        shark_count = np.count_nonzero(grid == "S")

        self.label_fish.config(text=f"Fish: {fish_count}")
        self.label_shark.config(text=f"Sharks: {shark_count}")



if __name__ == "__main__":
    root = tk.Tk()
    viewer = WatorViewerFast(root)
    root.mainloop()
