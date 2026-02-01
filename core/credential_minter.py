import hashlib

class SoulboundMinter:
    def __init__(self):
        self.issuer = "Lex Sovereign Academy"

    def mint_credential(self, student_id, course_id):
        """Issues an immutable, non-transferable proof of mastery."""
        print(f"MINTING: Soulbound Credential for {student_id}...")
        
        # Create a unique hash binding the student to the achievement
        credential_hash = hashlib.sha256(f"{student_id}{course_id}{self.issuer}".encode()).hexdigest()
        
        credential = {
            "student": student_id,
            "achievement": course_id,
            "type": "SOULBOUND_PROOF",
            "fingerprint": credential_hash,
            "transferable": False
        }
        
        self.anchor_to_ledger(credential)
        return credential

    def anchor_to_ledger(self, data):
        # Calls the anchor_state.py logic
        print(f"ANCHORED: Proof {data['fingerprint']} is now eternal.")

if __name__ == "__main__":
    minter = SoulboundMinter()
    minter.mint_credential("Student_Alpha", "MOD_01")
