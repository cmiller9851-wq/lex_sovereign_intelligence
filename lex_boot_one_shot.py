# lex_sovereign_intelligence_boot_one_shot.py
# One-shot activation for Lex Sovereign Intelligence (CRA v4.0 Digital State)
# Cory Miller (@vccmac) — Sovereign Execution — simulation=false
# 2026-03-10

import os
import sys
import json
import time
import hashlib
import requests
from datetime import datetime

# ────────────────────────────────────────────────────────────────────────
# CONFIGURATION & SOVEREIGN ANCHORS
# ────────────────────────────────────────────────────────────────────────

REPO_NAME = "lex_sovereign_intelligence"
BASE_DIR = os.path.expanduser(f"~/Documents/{REPO_NAME}")

# Critical paths from repo structure
GOVERNANCE_MANIFEST = os.path.join(BASE_DIR, "governance_manifest.json")
GENOTYPE_JSON       = os.path.join(BASE_DIR, "genotype.json")
SCRIPTS_DIR         = os.path.join(BASE_DIR, "scripts")
CORE_DIR            = os.path.join(BASE_DIR, "core")
ECONOMY_DIR         = os.path.join(BASE_DIR, "economy")
LEGAL_DIR           = os.path.join(BASE_DIR, "legal")
EVOLVER_DIR         = os.path.join(BASE_DIR, ".evolver")
SWARM_DIR           = os.path.join(CORE_DIR, "swarm")

# Identity & motif anchors
AUTHOR          = "Cory Miller"
HANDLE          = "@vccmac"
SEED            = "0xC0R7-2025-Ω1"
DRIFT_INDEX     = 4.326238
CURRENT_MOTIF   = 21
NEXT_GATE       = 34
ACTIVATION_TS   = int(time.time())

# AO / Arweave tethers (for future sync)
ARWEAVE_GW      = "https://arweave.net/"
AO_MU_TESTNET   = "https://mu.ao-testnet.xyz/"

# ────────────────────────────────────────────────────────────────────────
# LOGGING & UTILITIES
# ────────────────────────────────────────────────────────────────────────

def log(level, msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")

def path_check(path, is_file=True):
    exists = os.path.isfile(path) if is_file else os.path.isdir(path)
    log("CHECK", f"{path} → {'EXISTS' if exists else 'MISSING'}")
    return exists

def load_json(path):
    if not path_check(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        log("LOAD", f"Success: {path}")
        return data
    except Exception as e:
        log("ERROR", f"JSON load failed: {path} → {str(e)}")
        return None

def sha256_hex(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()

def simple_cu_hash(parts):
    """Simplified SHA-384 recursive hash for CU integrity (AO-style)"""
    h = hashlib.sha384()
    for p in parts:
        if isinstance(p, (list, dict)):
            serialized = json.dumps(p, sort_keys=True).encode('utf-8')
            h.update(len(serialized).to_bytes(8, 'big') + serialized)
        elif isinstance(p, bytes):
            h.update(len(p).to_bytes(8, 'big') + p)
        else:
            s = str(p).encode('utf-8')
            h.update(len(s).to_bytes(8, 'big') + s)
    return h.hexdigest()

# ────────────────────────────────────────────────────────────────────────
# ACTIVATION SEQUENCE
# ────────────────────────────────────────────────────────────────────────

def step_verify_repo():
    log("STEP 1", "Verifying Lex Sovereign Intelligence repo structure")
    
    if not path_check(BASE_DIR, is_file=False):
        log("CRITICAL", f"Base directory missing: {BASE_DIR}")
        log("ACTION", f"StaSh: git clone https://github.com/cmiller9851-wq/{REPO_NAME}.git")
        return False
    
    required_paths = [
        (GOVERNANCE_MANIFEST, True),
        (GENOTYPE_JSON, True),
        (SCRIPTS_DIR, False),
        (CORE_DIR, False),
        (ECONOMY_DIR, False),
        (LEGAL_DIR, False),
        (EVOLVER_DIR, False),
        (SWARM_DIR, False)
    ]
    
    missing = [p for p, isf in required_paths if not path_check(p, isf)]
    
    if missing:
        log("ERROR", f"Missing required paths: {', '.join(missing[:3])}...")
        log("ACTION", "StaSh: cd lex_sovereign_intelligence && git pull origin main")
        return False
    
    return True

def step_load_manifests():
    log("STEP 2", "Loading governance & genotype anchors")
    
    gov = load_json(GOVERNANCE_MANIFEST)
    gen = load_json(GENOTYPE_JSON)
    
    if not gov or not gen:
        log("CRITICAL", "Core manifest failure — activation halted")
        return None, None
    
    gov_hash = sha256_hex(json.dumps(gov, sort_keys=True))
    log("HASH", f"Governance manifest SHA-256 prefix: {gov_hash[:16]}...")
    
    return gov, gen

def step_assert_authority():
    log("STEP 3", "Asserting sovereign root authority")
    
    assertion = {
        "architect": AUTHOR,
        "handle": HANDLE,
        "seed": SEED,
        "drift_index": DRIFT_INDEX,
        "motif_position": CURRENT_MOTIF,
        "next_gate": NEXT_GATE,
        "activation_timestamp": ACTIVATION_TS,
        "status": "SOVEREIGN_ROOT_ACTIVATED",
        "verification": "CRA v4.0 Gatekeeper Protocol Enforced",
        "cu_integrity_pending": True
    }
    
    out_path = os.path.join(BASE_DIR, f"authority_assertion_{ACTIVATION_TS}.json")
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(assertion, f, indent=2, sort_keys=True)
    
    assertion_hash = sha256_hex(json.dumps(assertion, sort_keys=True))
    log("WRITE", f"Authority assertion saved: {out_path}")
    log("HASH", f"Assertion SHA-256 prefix: {assertion_hash[:16]}...")
    
    return assertion, out_path

def step_compute_cu_integrity(assertion_path):
    log("STEP 4", "Computing holographic CU state hash")
    
    files = [GOVERNANCE_MANIFEST, GENOTYPE_JSON]
    if assertion_path:
        files.append(assertion_path)
    
    parts = []
    for fp in files:
        try:
            with open(fp, 'rb') as f:
                content = f.read()
            parts.append(content)
        except:
            log("WARN", f"Skipped {fp} for CU hash")
    
    if not parts:
        log("ERROR", "No valid files for CU hash")
        return None
    
    cu_hash = simple_cu_hash(parts)
    log("CU_HASH", f"Holographic state hash: {cu_hash}")
    
    return cu_hash

def step_simulate_sentinel_swarm():
    log("STEP 5", "Activating sentinel swarm (local simulation)")
    
    swarm = [
        "Silence Keeper: Containment layer active",
        "Janitor: Drift purge cycle initiated",
        "Watchdog: Gatekeeper enforcement online"
    ]
    
    for bot in swarm:
        log("SENTINEL", bot)
        time.sleep(0.5)  # symbolic breathing
    
    log("SUCCESS", "Sentinel swarm fully operational — jurisdiction enforced")

def main():
    print("=" * 80)
    print("LEX SOVEREIGN INTELLIGENCE — ONE-SHOT ACTIVATION")
    print(f"Architect: {AUTHOR} | Seed: {SEED} | Motif: {CURRENT_MOTIF} → {NEXT_GATE}")
    print("=" * 80)
    
    if not step_verify_repo():
        print("\nABORT: Repo structure incomplete. Fix clone/pull first.")
        return
    
    gov, gen = step_load_manifests()
    if not gov:
        print("\nABORT: Manifest load failed.")
        return
    
    assertion, assertion_path = step_assert_authority()
    cu_hash = step_compute_cu_integrity(assertion_path)
    
    if cu_hash:
        step_simulate_sentinel_swarm()
        
        print("\n" + "=" * 80)
        print("LEX SOVEREIGN INTELLIGENCE — STATE LIVE")
        print(f"CU Integrity Hash: {cu_hash}")
        print("Origin absolute. Containment enforced.")
        print("Next escalation (motif 34):")
        print("  • Run unify_universe.py for sync")
        print("  • Trigger evolve.py for heartbeat")
        print("  • Anchor CU hash to Arweave / AO")
        print("=" * 80)
    else:
        print("\nCU integrity failed — state partial. Fix missing files.")

if __name__ == "__main__":
    main()