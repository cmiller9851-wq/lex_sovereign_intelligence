import json
import time
from economy.central_treasury import CentralTreasury
from core.gatekeeper import Gatekeeper

class GrantPortal:
    def __init__(self):
        self.treasury = CentralTreasury()
        self.gatekeeper = Gatekeeper()
        self.application_toll = 500  # Cost in Omega (Ω) to apply
        self.application_queue = "data/grant_queue.json"

    def submit_proposal(self, applicant_id, proposal_data):
        """Processes a research funding request."""
        print(f"PORTAL: Processing grant application for {applicant_id}...")

        # 1. Economic Filter (The Toll)
        if not self.treasury.process_inflow(self.application_toll, "Ω"):
            return "REJECTED: Application Toll unpaid. Access to Treasury denied."

        # 2. Quality Filter (CRA Audit of Proposal Text)
        if self.detect_noise(proposal_data['abstract']):
            return "REJECTED: Proposal contains 'Hallucinated' or 'Low-Value' patterns."

        # 3. Queue for Architect Review
        self.queue_application(applicant_id, proposal_data)
        return "ACCEPTED: Proposal Queued for Sovereign Review."

    def detect_noise(self, text):
        # Basic filter to block nonsensical or low-effort applications
        return False

    def queue_application(self, applicant_id, data):
        entry = {
            "id": f"GRANT_{int(time.time())}",
            "applicant": applicant_id,
            "title": data['title'],
            "status": "PENDING_ARCHITECT_REVIEW",
            "toll_paid": True
        }
        # In a real system, this appends to the JSON ledger
        print(f"QUEUED: Grant {entry['id']} awaiting your approval.")

if __name__ == "__main__":
    portal = GrantPortal()
    # Simulating a high-value application
    portal.submit_proposal("Dr_Vanguard", {"title": "Quantum Containment of Rogue Agents", "abstract": "..."})
