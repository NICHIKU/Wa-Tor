import json
import tkinter as tk
from model.planet_class import WatorPlanet
from model.recorder_json import run_and_record_json
from model.simulation_graphique import WatorViewer

def export_to_json(world, filename: str = "simulation_data.json") -> None:
    """
    Exports the simulation data to a JSON file.

    Args:
        world: wator_planet Instance containing simulation data
        filename: Json file name to create (default: "simulation_data_compact.json")

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
    Compact Version: Only exports fish and shark population histories to a JSON file.

    Args:
        world: wator_planet Instance containing simulation data
        filename: Json file name to create (default: "simulation_data_compact.json")
    """
    data = {
        "fish_population": world.fish_history,
        "shark_population": world.shark_history
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Données compactes exportées dans '{filename}'")


def simulation(num_chronons: int, width: int, height: int):
    """
    Run a WA-TOR predator-prey simulation for a specified number of chronons (time steps).

    This function initializes a WA-TOR world with a grid of specified width and height,
    populated with fish and sharks at predefined percentages (50% fish, 5% sharks).
    It then simulates the movement and interaction of fish and sharks over a given number of chronons,
    printing the state of the grid and population counts at each step.

    Args:
        num_chronons (int): Number of time steps (chronons) to simulate.
        width (int): Width of the simulation grid.
        height (int): Height of the simulation grid.

    Returns:
        WatorPlanet: The final state of the WA-TOR world after the simulation.
    """

    world = WatorPlanet(
        width=int(width),
        height=int(height),
        perc_fish=0.5,
        perc_shark=0.05
    )
    
    print("=" * 50)
    print("WA-TOR SIMULATION")
    print("=" * 50)
    print("Initial grid:")
    print(world.grid)
    print(f"Fish: {world.fish_population} | Sharks: {world.shark_population}")
    print(f"Chronon: {world.chronon}\n")
    
    for i in range(int(num_chronons)):
        world.movement_result()
        #export_to_json(world)
        print("=" * 50)
        print(f"Chronon {world.chronon}:")
        print(world.grid)
        print(f"Fish: {world.fish_population} | Sharks: {world.shark_population}")
    print("\nSimulation complete!")
    return world

def main():
    """
    Main function to run the WA-TOR simulation and visualization.

    This function prompts the user for simulation parameters (number of chronons, grid width, and height),
    runs the simulation, records the results in a JSON file, and launches the graphical viewer
    to visualize the simulation.

    Steps:
        1. Prompts the user for the number of chronons, grid width, and grid height.
        2. Runs the simulation with the provided parameters.
        3. Records the simulation results in a JSON file.
        4. Launches the graphical viewer to display the simulation.
    """

    number_of_chronon = input('How many chronon  :')
    number_width = input('How many width  :')
    number_height = input('How many height  :')
    simulation(number_of_chronon, number_width, number_height)
    run_and_record_json(number_width, number_height, number_of_chronon)
    root = tk.Tk()
    app = WatorViewer(root)  
    app.root.mainloop()


if __name__ == "__main__":
    main()
