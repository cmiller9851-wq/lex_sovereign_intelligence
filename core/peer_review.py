class PeerReviewConsensus:
    def __init__(self):
        self.required_votes = 3 # Number of Tenured Fellows needed to approve
    
    def review_submission(self, paper_id, reviews):
        """Aggregates scores from Tenured Fellows."""
        print(f"CONSENSUS: Tallying votes for Paper {paper_id}...")
        
        approve_count = 0
        for review in reviews:
            if review['verdict'] == 'APPROVE' and review['reviewer_rank'] == 'TENURED':
                approve_count += 1
        
        if approve_count >= self.required_votes:
            return "PUBLISH: Consenus reached. Anchoring to Arweave."
        else:
            return "REJECT: Insufficient peer validation."

if __name__ == "__main__":
    consensus = PeerReviewConsensus()
    # Simulating a vote
    votes = [
        {"reviewer_rank": "TENURED", "verdict": "APPROVE"},
        {"reviewer_rank": "TENURED", "verdict": "APPROVE"},
        {"reviewer_rank": "TENURED", "verdict": "APPROVE"}
    ]
    print(consensus.review_submission("Paper_XYZ", votes))
