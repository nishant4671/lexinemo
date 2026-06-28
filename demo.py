import sys
from pathlib import Path

# Add code directory to path
sys.path.append(str(Path(__file__).parent / "code"))

from src.agents.crew import run_compliance_check
from src.ui.app import mask_pii
import json

def run_demo():
    print("="*60)
    print(" L E X I N E M O   -   L I V E   D E M O ")
    print("="*60)
    
    # 1. Provide a raw, messy contract clause
    raw_clause = """
    7.4 Liability. The vendor's maximum liability for any data breaches 
    involving the customer's database (including the 5,000 users at 
    alex.doe@enterprise.in and phone +919876543210) shall be capped at 
    Rs. 10,000. No further claims will be entertained.
    """
    
    print("\n[1] RAW CONTRACT CLAUSE:")
    print("-" * 40)
    print(raw_clause.strip())
    
    # 2. Mask PII
    print("\n[2] PII MASKING (Presidio/Regex step):")
    print("-" * 40)
    masked_clause = mask_pii(raw_clause)
    print(masked_clause.strip())
    
    # 3. Run the AI Pipeline
    regulations = ["DPDP Act 2023"]
    print(f"\n[3] RUNNING CREW AI PIPELINE against {regulations}...")
    print("   -> Initiating Legal Researcher (with Web Search & Hybrid RAG)")
    print("   -> Initiating Compliance Assessor (Edge Case Detection)")
    print("   -> Initiating Corporate Communications Lead (Drafting)")
    print("-" * 40)
    
    # Run the compliance check
    result = run_compliance_check(masked_clause, regulations)
    
    # 4. Display Results
    print("\n[4] FINAL COMPLIANCE REPORT:")
    print("=" * 60)
    print(f"Overall Score: {result.get('score')}/100")
    print(f"Status:       {result['clauses'][0]['status'].upper()}")
    print("-" * 60)
    print("REASON FOR FLAG:")
    print(result['clauses'][0]['reason'])
    print("-" * 60)
    print("GENERATED EMAIL DRAFT FOR VENDOR:")
    print(result.get('email_draft', 'No email generated.'))
    print("=" * 60)
    print("\nDemo Complete! The Streamlit UI does exactly this, but with interactive buttons and PDF downloads.")

if __name__ == "__main__":
    run_demo()
