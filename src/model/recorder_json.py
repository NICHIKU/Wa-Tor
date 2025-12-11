import json
import os
from datetime import datetime
from .planet_class import WatorPlanet   # adapte si ton fichier ne s'appelle pas wator.py

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_and_record_json(width, height, chronons, perc_fish=0.5, perc_shark=0.05):
    world = WatorPlanet(width=int(width), height=int(height), 
                         perc_fish=perc_fish, perc_shark=perc_shark)

    history = []

    history.append(world.grid.tolist())

    for _ in range(int(chronons)):
        world.movement_result()
        history.append(world.grid.tolist())

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(OUTPUT_DIR, f"wator_history_grid_{timestamp}_number_of_chronons_{chronons}_size_height{height}x{width}.json")

    data = {
        "width": width,
        "height": height,
        "chronons": chronons,
        "history": history
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"OK Simulation enregistrée dans:\n → {out_path}")
    print(f"Chronons enregistrées: {len(history) - 1}")

    return out_path

if __name__ == "__main__":
    run_and_record_json()