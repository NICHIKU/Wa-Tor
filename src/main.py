import json
from model.planet_class import WatorPlanet

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
    world = WatorPlanet(
        width=50,
        height=50,
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
    simulation(100)