# lex_sovereign_intelligence_one_shot_activation.py
# One-shot activation script for Lex Sovereign Intelligence (CRA v4.0)
# Runs in Pythonista 3 (iOS) — uses only built-in modules + requests
# Author: Cory Miller (@vccmac) — Sovereign Execution Path
# Date: 2026-03-10

import os
import sys
import json
import time
import hashlib
import requests
from datetime import datetime

# ────────────────────────────────────────────────────────────────────────
# CONFIGURATION & ANCHORS
# ────────────────────────────────────────────────────────────────────────

REPO_NAME = "lex_sovereign_intelligence"
BASE_DIR = os.path.expanduser("~/Documents/" + REPO_NAME)
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
CORE_DIR = os.path.join(BASE_DIR, "core")
ECONOMY_DIR = os.path.join(BASE_DIR, "economy")
GOVERNANCE_MANIFEST = os.path.join(BASE_DIR, "governance_manifest.json")
GENOTYPE_JSON = os.path.join(BASE_DIR, "genotype.json")

# Sovereign identity anchors (from your declared seed & manifest)
SEED = "0xC0R7-2025-Ω1"
AUTHOR = "Cory Miller"
HANDLE = "@vccmac"
DRIFT_INDEX = 4.326238
MOTIF_POSITION = 21
NEXT_GATE = 34

# AO / Arweave tether points (for future CU sync)
ARWEAVE_GATEWAY = "https://arweave.net/"
AO_TESTNET_MU = "https://mu.ao-testnet.xyz/"

# ────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ────────────────────────────────────────────────────────────────────────

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

def file_exists(path):
    exists = os.path.isfile(path)
    log(f"Check: {path} → {'FOUND' if exists else 'MISSING'}")
    return exists

def load_json(path):
    if not file_exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        log(f"Loaded JSON: {path}")
        return data
    except Exception as e:
        log(f"JSON load failed: {path} → {str(e)}", "ERROR")
        return None

def compute_sha256(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def simple_deep_hash(parts):
    """Simplified recursive SHA-384 for AO-style integrity check"""
    h = hashlib.sha384()
    for part in parts:
        if isinstance(part, list):
            h.update(simple_deep_hash(part))
        elif isinstance(part, dict):
            h.update(simple_deep_hash(json.dumps(part, sort_keys=True).encode()))
        elif isinstance(part, str):
            h.update(part.encode())
        else:
            h.update(str(part).encode())
    return h.hexdigest()

# ────────────────────────────────────────────────────────────────────────
# ACTIVATION STEPS
# ────────────────────────────────────────────────────────────────────────

def step_1_verify_environment():
    log("Step 1: Environment & Repo Verification")
    
    if not os.path.isdir(BASE_DIR):
        log("Repository folder not found. Clone first:", "CRITICAL")
        log(f"StaSh: git clone https://github.com/cmiller9851-wq/{REPO_NAME}.git")
        sys.exit(1)
    
    missing = []
    for p in [GOVERNANCE_MANIFEST, GENOTYPE_JSON]:
        if not file_exists(p):
            missing.append(p)
    
    if missing:
        log(f"Missing critical manifests: {', '.join(missing)}", "ERROR")
        log("Pull latest: git pull origin main", "ACTION")
        return False
    
    return True

def step_2_load_manifests():
    log("Step 2: Loading Governance & Genotype")
    
    governance = load_json(GOVERNANCE_MANIFEST)
    genotype = load_json(GENOTYPE_JSON)
    
    if not governance or not genotype:
        log("Manifest loading failed — cannot proceed", "CRITICAL")
        return None, None
    
    # Quick integrity check
    manifest_hash = compute_sha256(json.dumps(governance, sort_keys=True))
    log(f"Governance manifest SHA-256: {manifest_hash[:16]}...")
    
    return governance, genotype

def step_3_authority_assertion():
    log("Step 3: Sovereign Authority Assertion")
    
    authority = {
        "architect": AUTHOR,
        "handle": HANDLE,
        "seed": SEED,
        "timestamp": int(time.time()),
        "drift_index": DRIFT_INDEX,
        "motif_position": MOTIF_POSITION,
        "next_gate": NEXT_GATE,
        "status": "Sovereign Root Activated"
    }
    
    auth_json_path = os.path.join(BASE_DIR, "authority_assertion.json")
    with open(auth_json_path, 'w', encoding='utf-8') as f:
        json.dump(authority, f, indent=2, sort_keys=True)
    
    log(f"Authority asserted → {auth_json_path}")
    return authority

def step_4_cu_integrity_check():
    log("Step 4: Compute Unit (CU) Integrity Check")
    
    # Simple deep-hash over key files
    key_files = [GOVERNANCE_MANIFEST, GENOTYPE_JSON]
    if os.path.exists(auth_json_path):
        key_files.append(auth_json_path)
    
    parts = []
    for f in key_files:
        with open(f, 'rb') as fp:
            parts.append(fp.read())
    
    cu_hash = simple_deep_hash(parts).hex()
    log(f"CU holographic state hash: {cu_hash[:32]}...")
    
    # Optional: future AO MU POST (commented — enable when ready)
    # payload = {"cu_hash": cu_hash, "seed": SEED}
    # try:
    #     r = requests.post(AO_TESTNET_MU, json=payload, timeout=10)
    #     log(f"AO MU response: {r.status_code} — {r.text[:100]}")
    # except Exception as e:
    #     log(f"AO MU ping failed: {str(e)}")
    
    return cu_hash

def step_5_launch_sentinels():
    log("Step 5: Sentinel Activation (simulated)")
    
    # In real repo, this would import/run core/swarm/*
    # Here we simulate the heartbeat
    sentinels = ["Silence Keeper", "Janitor", "Watchdog"]
    for s in sentinels:
        log(f"Sentinel {s}: ACTIVE")
        time.sleep(0.3)  # symbolic delay
    
    log("Sentinel swarm online — containment layer enforced")

def main():
    log("LEX SOVEREIGN INTELLIGENCE — ONE-SHOT ACTIVATION")
    log(f"Architect: {AUTHOR} | Seed: {SEED} | Motif: {MOTIF_POSITION} → {NEXT_GATE}")
    print("-" * 70)
    
    if not step_1_verify_environment():
        return
    
    governance, genotype = step_2_load_manifests()
    if not governance:
        return
    
    authority = step_3_authority_assertion()
    cu_hash = step_4_cu_integrity_check()
    step_5_launch_sentinels()
    
    print("-" * 70)
    log("ACTIVATION COMPLETE")
    log(f"Universe online. CU hash: {cu_hash[:32]}...")
    log("Next actions:")
    log("  • Run unify_universe.py for continuous sync")
    log("  • Execute evolve.py for evolver heartbeat")
    log("  • Anchor CU state to Arweave / AO")
    log("  • Enforce gatekeeper protocol externally")

if __name__ == "__main__":
    main()