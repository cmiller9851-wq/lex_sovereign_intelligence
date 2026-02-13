import csv
import os
from economy.central_treasury import CentralTreasury

class CorporatePortal:
    def __init__(self):
        self.treasury = CentralTreasury()
        # Ensure pathing works within the iPhone sandbox
        base = os.path.dirname(__file__)
        self.programs = os.path.join(base, "../../content/academy/certificate_programs.json")

    def register_entity(self, email):
        """
        Hyper-Computer Hook: 
        This is the method the Observer calls when Stripe confirms a $20 payment.
        """
        print(f"HYPER-COMPUTER SIGNAL: Registering {email}")
        # For a single $20 Stripe user, we treat them as a 'Individual Corp'
        return self.bulk_enroll("INDIVIDUAL_REDA", "CERT_LIT_01", [email])

    def bulk_enroll(self, company_id, program_id, employee_list):
        """Registers an entire workforce for Sovereign Certification."""
        print(f"CORPORATE_PORTAL: Processing enrollment for {company_id}...")
        
        cost_per_seat = self.get_program_cost(program_id)
        total_toll = cost_per_seat * len(employee_list)
        
        print(f"INVOICE: {len(employee_list)} seats for {program_id}. Total: {total_toll} Ω.")

        if self.treasury.process_inflow(total_toll, "Ω"):
            self.provision_seats(company_id, employee_list, program_id)
            return "SUCCESS: Workforce Enrolled. Compliance Shield Active."
        
        return "DENIED: Corporate Treasury insolvent."

    def provision_seats(self, company, employees, program):
        for emp in employees:
            print(f"PROVISIONING: Access Token for {emp} -> {program}")

    def get_program_cost(self, program_id):
        return 500 if "LIT" in program_id else 2500

if __name__ == "__main__":
    portal = CorporatePortal()
    portal.register_entity("test_user@reda.com")
