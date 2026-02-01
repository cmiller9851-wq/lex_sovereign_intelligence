import json
import os

def set_gatekeeper():
    authority = {
        "gatekeeper": "Cory Michael Miller",
        "role": "Root Architect",
        "inheritance_locked": True,
        "governance": "CRA v4.0"
    }
    
    os.makedirs(".evolver", exist_ok=True)
    with open(".evolver/authority_root.json", "w") as f:
        json.dump(authority, f, indent=4)
    
    print("Authority Established: Lex Sovereign Intelligence is now active under the Gatekeeper.")

if __name__ == "__main__":
    set_gatekeeper()
