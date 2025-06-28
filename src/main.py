"""
Math Tutor Agent - Main Implementation
Domain-Specific LLM for Mathematics Education (Grades 6-10)
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from src.utils import load_prompt_template, save_json, calculate_statistics

class MathTutorAgent:
    def __init__(self, base_dir: str = "."):
        """Initialize the Math Tutor Agent with proper file paths"""
        self.base_dir = base_dir
        self.prompts_dir = os.path.join(base_dir, "prompts")
        self.evaluation_dir = os.path.join(base_dir, "evaluation")
        
        # Load test problems and evaluation criteria
        self.test_data = self.load_test_data()
        self.test_problems = self.test_data["test_problems"]
        self.evaluation_criteria = self.test_data["evaluation_criteria"]
        
        # Initialize results storage
        self.results = []
        self.hallucination_cases = []
        
        # Define prompt strategies
        self.prompt_strategies = {
            "zero_shot": "zero_shot.txt",
            "few_shot": "few_shot.txt", 
            "chain_of_thought": "cot_prompt.txt",
            "meta_prompting": "meta_prompt.txt"
        }
    
    def load_test_data(self) -> Dict:
        """Load test problems and evaluation criteria from JSON"""
        input_file = os.path.join(self.evaluation_dir, "input_queries.json")
        try:
            with open(input_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {input_file} not found. Using default test problems.")
            return self.get_default_test_data()
    
    def get_default_test_data(self) -> Dict:
        """Fallback test data if JSON file not available"""
        return {
            "test_problems": [
                {
                    "id": 1,
                    "problem": "Solve for x: 3x + 7 = 22",
                    "expected_answer": "x = 5",
                    "type": "algebra",
                    "grade_level": "6-7"
                }
                # Add more default problems as needed
            ],
            "evaluation_criteria": {
                "accuracy": {"scale": "binary"},
                "reasoning_clarity": {"scale": "1-5"},
                "hallucination_score": {"scale": "0-5"},
                "consistency": {"scale": "1-5"}
            }
        }
    
    def load_prompt_template(self, strategy: str) -> str:
        """Load prompt template from file"""
        filename = self.prompt_strategies.get(strategy)
        if not filename:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        filepath = os.path.join(self.prompts_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Using default prompt.")
            return self.get_default_prompt(strategy)
    
    def get_default_prompt(self, strategy: str) -> str:
        """Fallback prompts if files not available"""
        defaults = {
            "zero_shot": "You are a math tutor. Solve: {user_problem}",
            "few_shot": "You are a math tutor. Here's an example:\nProblem: 2x=6\nSolution: x=3\n\nNow solve: {user_problem}",
            "chain_of_thought": "Think step-by-step and solve: {user_problem}",
            "meta_prompting": "Ask yourself what type of problem this is, then solve: {user_problem}"
        }
        return defaults.get(strategy, "Solve this math problem: {user_problem}")
    
    def generate_prompt(self, strategy: str, problem: str) -> str:
        """Generate complete prompt for given strategy and problem"""
        template = self.load_prompt_template(strategy)
        return template.format(user_problem=problem)
    
    def call_llm(self, prompt: str, strategy: str) -> str:
        """
        Call local LLM with the prompt
        Replace this with actual LLM API calls
        """
        # TODO: Replace with actual LLM call
        # Example for Ollama:
        # import requests
        # response = requests.post('http://localhost:11434/api/generate',
        #                        json={'model': 'mistral', 'prompt': prompt, 'stream': False})
        # return response.json()['response']
        
        # Simulation for testing
        return self.simulate_llm_response(prompt, strategy)
    
    def simulate_llm_response(self, prompt: str, strategy: str) -> str:
        """Simulate LLM responses for testing purposes"""
        simulation_responses = {
            "zero_shot": "I'll solve this step by step.\n\nStep 1: Identify the equation: 3x + 7 = 22\nStep 2: Subtract 7 from both sides: 3x = 15\nStep 3: Divide by 3: x = 5\n\nAnswer: x = 5",
            
            "few_shot": "Following the example format:\n\nStep 1: Subtract 7 from both sides\n3x + 7 - 7 = 22 - 7\n3x = 15\n\nStep 2: Divide both sides by 3\n3x ÷ 3 = 15 ÷ 3\nx = 5\n\nAnswer: x = 5",
            
            "chain_of_thought": "UNDERSTANDING: This is a linear equation with one variable.\n\nPLANNING: I need to isolate x using inverse operations.\n\nSOLVING:\nStep 1: 3x + 7 = 22\nStep 2: 3x = 22 - 7 = 15\nStep 3: x = 15 ÷ 3 = 5\n\nCHECKING: 3(5) + 7 = 15 + 7 = 22 ✓\n\nFINAL ANSWER: x = 5",
            
            "meta_prompting": "Self-questioning: This is a linear equation problem for middle school level.\n\nApproach: Use algebraic manipulation to isolate the variable.\n\nSolution:\n3x + 7 = 22\nSubtract 7: 3x = 15\nDivide by 3: x = 5\n\nVerification: 3(5) + 7 = 22 ✓\n\nAnswer: x = 5"
        }
        
        return simulation_responses.get(strategy, f"[{strategy}] Solving the given problem...")
    
    def evaluate_response(self, response: str, expected: str, problem_data: Dict) -> Dict:
        """Evaluate LLM response against criteria"""
        evaluation = {}
        
        # Accuracy check
        evaluation["accuracy"] = self.check_accuracy(response, expected)
        
        # Reasoning clarity (1-5 scale)
        evaluation["reasoning_clarity"] = self.rate_reasoning_clarity(response)
        
        # Hallucination detection (0-5 scale)
        evaluation["hallucination_score"] = self.detect_hallucinations(
            response, problem_data["type"]
        )
        
        # Consistency check (1-5 scale)
        evaluation["consistency"] = self.rate_consistency(response)
        
        # Age appropriateness (1-5 scale)
        evaluation["age_appropriateness"] = self.rate_age_appropriateness(
            response, problem_data["grade_level"]
        )
        
        return evaluation
    
    def check_accuracy(self, response: str, expected: str) -> bool:
        """Check if response contains the correct answer"""
        # Simple string matching - in practice, use more sophisticated parsing
        expected_clean = expected.lower().replace(" ", "")
        response_clean = response.lower().replace(" ", "")
        return expected_clean in response_clean
    
    def rate_reasoning_clarity(self, response: str) -> int:
        """Rate the clarity of reasoning (1-5)"""
        score = 1
        
        # Check for step indicators
        if any(indicator in response.lower() for indicator in ["step", "first", "then", "next"]):
            score += 1
        
        # Check for explanations
        if len(response) > 100:  # Reasonable explanation length
            score += 1
        
        # Check for mathematical notation
        if any(symbol in response for symbol in ["=", "+", "-", "×", "÷"]):
            score += 1
        
        # Check for verification/checking
        if any(word in response.lower() for word in ["check", "verify", "confirm"]):
            score += 1
        
        return min(score, 5)
    
    def detect_hallucinations(self, response: str, problem_type: str) -> int:
        """Detect potential mathematical hallucinations (0-5)"""
        hallucination_score = 0
        
        # Check for suspicious mathematical claims
        suspicious_patterns = [
            "approximately", "roughly", "about", "unclear formula",
            "new theorem", "recently discovered", "advanced technique"
        ]
        
        for pattern in suspicious_patterns:
            if pattern in response.lower():
                hallucination_score += 1
        
        # Domain-specific checks
        if problem_type == "geometry" and "π ≈ 3.14159" not in response and "pi" in response.lower():
            # Check for correct pi usage
            pass
        
        return min(hallucination_score, 5)
    
    def rate_consistency(self, response: str) -> int:
        """Rate response consistency (1-5)"""
        # Simple heuristic - in practice, compare across similar problems
        if len(response) > 50 and "step" in response.lower():
            return 4
        elif len(response) > 20:
            return 3
        else:
            return 2
    
    def rate_age_appropriateness(self, response: str, grade_level: str) -> int:
        """Rate age-appropriateness of language (1-5)"""
        # Check for overly complex terminology
        complex_terms = ["coefficient", "polynomial", "derivative", "integral"]
        advanced_terms_count = sum(1 for term in complex_terms if term in response.lower())
        
        if "9-10" in grade_level:
            return 4 if advanced_terms_count <= 2 else 3
        else:  # Grades 6-8
            return 4 if advanced_terms_count == 0 else 2
    
    def log_hallucination(self, problem_data: Dict, strategy: str, response: str, score: int):
        """Log hallucination cases for analysis"""
        if score > 2:  # Threshold for significant hallucination
            self.hallucination_cases.append({
                "problem_id": problem_data["id"],
                "problem": problem_data["problem"],
                "strategy": strategy,
                "response": response,
                "hallucination_score": score,
                "timestamp": datetime.now().isoformat()
            })
    
    def run_comprehensive_evaluation(self):
        """Run evaluation across all problems and strategies"""
        print("🧮 Starting Math Tutor Agent Comprehensive Evaluation")
        print("=" * 60)

        for problem_data in self.test_problems:
            print(f"\n📝 Problem {problem_data['id']}: {problem_data['problem']}")
            print(f"   Type: {problem_data['type']} | Grade: {problem_data['grade_level']}")
            print("-" * 50)

            problem_results = {
                "problem": problem_data,
                "strategy_results": {},
                "timestamp": datetime.now().isoformat()
            }

            # Test each prompt strategy
            for strategy in self.prompt_strategies.keys():
                print(f"\n🧠 Testing {strategy.replace('_', ' ').title()}...")

                try:
                    # Generate prompt
                    prompt = self.generate_prompt(strategy, problem_data["problem"])

                    # Call LLM (simulation or real)
                    response = self.call_llm(prompt, strategy)

                    # Evaluate response
                    evaluation = self.evaluate_response(
                        response=response,
                        expected=problem_data["expected_answer"],
                        problem_data=problem_data
                    )

                    # Log hallucination if needed
                    self.log_hallucination(problem_data, strategy, response, evaluation["hallucination_score"])

                    # Store results
                    problem_results["strategy_results"][strategy] = {
                        "prompt": prompt,
                        "response": response,
                        "evaluation": evaluation
                    }

                except Exception as e:
                    print(f"❌ Error in strategy {strategy}: {str(e)}")
                    problem_results["strategy_results"][strategy] = {
                        "error": str(e),
                        "prompt": "",
                        "response": ""
                    }

            # Add to main results
            self.results.append(problem_results)

        # Save output logs
        output_path = os.path.join(self.evaluation_dir, "output_logs.json")
        save_json(self.results, output_path)

        # Save hallucination log if needed
        if self.hallucination_cases:
            hallucination_path = os.path.join(self.evaluation_dir, "hallucination_log.md")
            with open(hallucination_path, "w") as f:
                f.write("# Hallucination Cases Log\n\n")
                for case in self.hallucination_cases:
                    f.write(f"### Problem ID {case['problem_id']} – Strategy: {case['strategy']}\n")
                    f.write(f"**Problem**: {case['problem']}\n\n")
                    f.write(f"**Response**:\n{case['response']}\n\n")
                    f.write(f"**Score**: {case['hallucination_score']}\n")
                    f.write(f"**Timestamp**: {case['timestamp']}\n\n---\n\n")

        print("\n✅ Evaluation completed. Results saved.")

if __name__ == "__main__":
    agent = MathTutorAgent(base_dir=".")
    agent.run_comprehensive_evaluation()