import os
import subprocess
import json

# Repositories to integrate into the Coherent System
UNIVERSE_REPOS = {
    "fusion-engine": "https://github.com/cmiller9851-wq/adaptive-knowledge-fusion-engine",
    "oracle": "https://github.com/cmiller9851-wq/v3-da-oracle",
}

def integrate_submodules():
    """Adds your other repos as git submodules if they don't exist."""
    print("Initiating Universe Integration...")
    for name, url in UNIVERSE_REPOS.items():
        dest = f"modules/{name}"
        if not os.path.exists(dest):
            subprocess.run(["git", "submodule", "add", url, dest])
            print(f"Integrated: {name}")
        else:
            print(f"Skipping: {name} (Already integrated)")

def generate_system_manifest():
    """Creates a manifest of all available protocols and logic paths."""
    manifest = {
        "system_id": "OMEGA-1",
        "owner": "Cory Michael Miller",
        "protocols": ["CRA-v4.0", "AKFE-v1", "V3-DA"],
        "active_modules": list(UNIVERSE_REPOS.keys())
    }
    with open("data/universe_map.json", "w") as f:
        json.dump(manifest, f, indent=4)
    print("Manifest Generated: data/universe_map.json")

if __name__ == "__main__":
    integrate_submodules()
    generate_system_manifest()
