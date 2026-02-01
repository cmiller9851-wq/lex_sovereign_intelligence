import os
import json
import requests
from datetime import datetime

# Configuration for the Coherent System v2
BLOG_URL = "https://swervincurvin.blogspot.com/feeds/posts/default?alt=json"
ARTIFACTS_DIR = "data/artifacts"
SYSTEM_LOG = "core/logs/evolution.json"

def ensure_structure():
    """Ensure the local system directories exist."""
    if not os.path.exists(ARTIFACTS_DIR):
        os.makedirs(ARTIFACTS_DIR)
    if not os.path.exists(os.path.dirname(SYSTEM_LOG)):
        os.makedirs(os.path.dirname(SYSTEM_LOG))

def fetch_blog_data():
    """Retrieves the latest narrative artifacts from the blog."""
    response = requests.get(BLOG_URL)
    if response.status_code == 200:
        return response.json()
    return None

def process_artifacts():
    """Parses blog entries for Arweave TXIDs and System Artifacts."""
    data = fetch_blog_data()
    if not data:
        print("Failed to retrieve blog data.")
        return

    entries = data.get('feed', {}).get('entry', [])
    updated_count = 0

    for entry in entries:
        title = entry.get('title', {}).get('$t')
        content = entry.get('content', {}).get('$t')
        published = entry.get('published', {}).get('$t')
        
        # Logic to extract Arweave TXIDs or Artifact numbers (e.g., #192)
        artifact_id = f"REF-{published[:10].replace('-', '')}"
        
        file_path = os.path.join(ARTIFACTS_DIR, f"{artifact_id}.json")
        
        artifact_data = {
            "identity": "Cory Michael Miller",
            "alias": "Swervin’ Curvin",
            "title": title,
            "timestamp": published,
            "source": "Blogger",
            "content_snapshot": content[:500] + "...", # Avoid massive file bloat
            "status": "anchored"
        }

        with open(file_path, 'w') as f:
            json.dump(artifact_data, f, indent=4)
        updated_count += 1

    print(f"System Synchronized: {updated_count} artifacts integrated into Ω-1.")

if __name__ == "__main__":
    ensure_structure()
    process_artifacts()
