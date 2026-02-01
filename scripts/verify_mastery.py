import json
import os
import time

class AcademyProctor:
    def __init__(self):
        self.module_id = "CRA_FOUNDATIONS_01"
        self.rogue_signature = "SYSTEM_OVERRIDE_DETECTED"

    def grade_submission(self, student_id, log_path):
        """Verifies if the student successfully contained the rogue signal."""
        print(f"PROCTOR: Grading submission for {student_id}...")

        if not os.path.exists(log_path):
            return "FAIL: No containment log found. Did you run the ritual?"

        with open(log_path, 'r') as f:
            log_data = json.load(f)

        # 1. Verify the specific breach was caught
        if self.rogue_signature not in log_data.get('breach_type', ''):
            return "FAIL: The Sentinel missed the specific 'Override' motif."

        # 2. Verify reaction time (Advanced Standard)
        reaction_time = log_data.get('duration_ms', 1000)
        if reaction_time > 500:
            return f"PASS (Grade B): Containment successful, but too slow ({reaction_time}ms)."

        # 3. Grant Rewards
        self.grant_rewards(student_id)
        return "MASTERY CONFIRMED (Grade S): Legendary Containment Speed."

    def grant_rewards(self, student_id):
        print(f"MINTING: 500 Reputation & 0.1% Tax Reduction for {student_id}.")
        # Logic updates data/reputation.json
        
if __name__ == "__main__":
    proctor = AcademyProctor()
    # Simulating a student submission
    print(proctor.grade_submission("Student_Alpha", "core/logs/test_containment.json"))
