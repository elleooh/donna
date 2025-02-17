from openai import OpenAI
from typing import Dict, List
import json
import os
from datetime import datetime

class NegotiationPlanner:
    def __init__(self):
        self.client = OpenAI()
        
    def get_completion(self, prompt: str, model: str = "o3-mini") -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert salary negotiation assistant, helping analyze situations and provide strategic advice."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    # Mock data functions that would normally connect to real APIs/databases
    def get_previous_calls(self) -> List[Dict]:
        transcript_folder = "transcripts"  # Adjust path as needed
        calls = []
        
        # Ensure folder exists
        if not os.path.exists(transcript_folder):
            return []
            
        # Read all txt files from the transcript folder
        for filename in os.listdir(transcript_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(transcript_folder, filename)
                try:
                    # Read file content as summary
                    with open(file_path, 'r') as f:
                        transcript = f.read().strip()
                        
                    # Use file modification time as date
                    mod_time = os.path.getmtime(file_path)
                    date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
                        
                    calls.append({
                        "date": date,
                        "transcript": transcript
                    })

                except Exception:
                    continue  # Skip files that can't be read
                    
        # Sort calls by date
        calls.sort(key=lambda x: x["date"])
        return calls
    
    def get_current_offer(self) -> Dict:
        return {
            "base_salary": 120000,
            "bonus": "15%",
            "equity": "10000 RSUs",
            "benefits": ["health", "dental", "401k match 6%"]
        }
    
    def get_market_data(self) -> Dict:
        return {
            "role_median": 135000,
            "role_range": "115000-155000",
            "industry_growth": "15%",
            "demand_level": "high"
        }

    def analyze_previous_calls(self) -> str:
        calls = self.get_previous_calls()
        prompt = f"""Analyze these previous interview calls and highlight key negotiation points that could be leveraged:
        {json.dumps(calls, indent=2)}
        
        Focus on:
        1. Key points discussed about compensation
        2. Any flexibility or hints mentioned by the recruiter
        3. Overall tone and receptiveness
        4. Specific promises or commitments made
        
        format output in markdown 
        """
        return self.get_completion(prompt)

    def analyze_market_position(self, call_summary: str) -> str:
        market_data = self.get_market_data()
        current_offer = self.get_current_offer()
        prompt = f"""Compare this offer to market data and identify negotiation leverage points:
        
        Current Offer: {json.dumps(current_offer, indent=2)}
        Market Data: {json.dumps(market_data, indent=2)}
        Previous Call Analysis: {call_summary}
        
        Focus on:
        1. Position relative to market median
        2. Industry trends and demand
        3. Compensation package competitiveness
        4. Specific areas where the offer could be improved
        
        format output in markdown 
        """
        return self.get_completion(prompt)

    def create_negotiation_plan(self, call_summary: str, market_analysis: str) -> str:
        current_offer = self.get_current_offer()
        prompt = f"""Create a detailed negotiation strategy based on the following information:
        
        Current Offer: {json.dumps(current_offer, indent=2)}
        Call History Analysis: {call_summary}
        Market Analysis: {market_analysis}
        
        Please provide:
        1. Primary negotiation targets with specific numbers
        2. Fallback positions and minimum acceptable terms
        3. Specific talking points and scripts
        4. Responses to potential objections
        5. Timeline and communication approach

        format output in markdown 
        """
        return self.get_completion(prompt)

    def generate_complete_plan(self) -> Dict[str, str]:
        # Step 1: Analyze previous calls
        call_summary = self.analyze_previous_calls()
        
        # Step 2: Analyze market position and current offer
        market_analysis = self.analyze_market_position(call_summary)
        
        # Step 3: Create negotiation plan
        negotiation_plan = self.create_negotiation_plan(call_summary, market_analysis)
        
        return {
            "call_summary": call_summary,
            "market_analysis": market_analysis,
            "negotiation_plan": negotiation_plan
        }

    def run_conversation(self, message: str) -> str:
        if not message.strip():
            raise ValueError("Message cannot be empty")
            
        response = self.client.chat.completions.create(
            model="o1",
            messages=[
                {"role": "system", "content": "You are an expert salary negotiation assistant. Provide clear, actionable advice based on the context of the negotiation."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content.strip() 