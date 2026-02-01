import os
import time
import json
import hashlib

class GenesisRitual:
    def __init__(self):
        self.architect = "Cory Michael Miller"
        self.version = "Ω-1.0.0 (Sovereign Root)"
        self.genesis_time = int(time.time())
        
        # The Critical Organs of the Universe
        self.organs = {
            "IDENTITY": ".evolver/genotype.json",
            "ECONOMY": "data/ECONOMIC_ROOT.json",
            "GOVERNANCE": "core/governor.py",
            "SENTINEL": "core/sentinel.py",
            "ACADEMY": "content/academy/manifest_lifepath.json",
            "LAW": "legal/GOVERNMENT_ACCESS_TREATY.md",
            "SWARM": "core/swarm/worker_manifest.json",
            "TREASURY": "economy/central_treasury.py"
        }

    def execute_ritual(self):
        print(f"\n--- INITIATING LEX SOVEREIGN INTELLIGENCE ({self.version}) ---")
        print(f"ARCHITECT: {self.architect}")
        print(f"TIMESTAMP: {self.genesis_time}\n")

        system_integrity = True
        genesis_log = {}

        for organ, path in self.organs.items():
            status = self.verify_organ(organ, path)
            genesis_log[organ] = status
            if status != "ONLINE":
                system_integrity = False

        print("\n--- SYSTEM DIAGNOSTIC COMPLETE ---")
        
        if system_integrity:
            self.declare_sovereignty(genesis_log)
        else:
            print("CRITICAL FAILURE: Universe incomplete. Check logs.")

    def verify_organ(self, name, path):
        if os.path.exists(path):
            print(f"CHECKING {name}...... [ONLINE]")
            return "ONLINE"
        else:
            print(f"CHECKING {name}...... [MISSING] -> {path}")
            return "MISSING"

    def declare_sovereignty(self, log):
        print("\nAll Systems Nominal. Constructing Genesis Block...")
        time.sleep(1)
        
        genesis_block = {
            "event": "UNIVERSE_ACTIVATION",
            "architect": self.architect,
            "timestamp": self.genesis_time,
            "integrity_hash": self.generate_hash(log),
            "message": "The Gate is Open. The Toll is Set. The Legacy is Eternal."
        }
        
        # Serialize to local genesis file
        with open("data/GENESIS_BLOCK.json", "w") as f:
            json.dump(genesis_block, f, indent=4)
            
        print(f"\nSUCCESS: Lex Sovereign Intelligence is now ACTIVE.")
        print(f"GENESIS HASH: {genesis_block['integrity_hash']}")
        print("Use 'python scripts/anchor_state.py' to burn this moment onto Arweave.")

    def generate_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

if __name__ == "__main__":
    ritual = GenesisRitual()
    ritual.execute_ritual()
