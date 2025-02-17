from agents.agent_config import NegotiationPlanner
import json
import os

def print_section(title: str, content: str):
    print("\n" + "="*50)
    print(f"{title}")
    print("="*50)
    print(content)

def main():
    # Initialize the negotiation planner
    planner = NegotiationPlanner()
    
    print("Starting Salary Negotiation Analysis...\n")
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Display and save current offer
    current_offer = planner.get_current_offer()
    print_section("Current Offer", json.dumps(current_offer, indent=2))
    
    # Display and save market data
    market_data = planner.get_market_data()
    print_section("Market Data", json.dumps(market_data, indent=2))
    
    # Generate complete negotiation plan
    print("\nGenerating comprehensive negotiation plan...")
    plan = planner.generate_complete_plan()
    
    # Display the results and save to files
    print_section("Previous Calls Analysis", plan['call_summary'])
    with open(os.path.join(output_dir, "call_summary.txt"), "w") as f:
        f.write(plan['call_summary'])
    
    print_section("Market Position Analysis", plan['market_analysis'])
    with open(os.path.join(output_dir, "market_analysis.txt"), "w") as f:
        f.write(plan['market_analysis'])
    
    print_section("Negotiation Strategy", plan['negotiation_plan'])
    with open(os.path.join(output_dir, "negotiation_strategy.txt"), "w") as f:
        f.write(plan['negotiation_plan'])
    
    # Save the complete plan
    with open(os.path.join(output_dir, "complete_plan.txt"), "w") as f:
        f.write("=== Previous Calls Analysis ===\n")
        f.write(plan['call_summary'])
        f.write("\n\n=== Market Position Analysis ===\n")
        f.write(plan['market_analysis'])
        f.write("\n\n=== Negotiation Strategy ===\n")
        f.write(plan['negotiation_plan'])

if __name__ == "__main__":
    main() 