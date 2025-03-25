from autogen import autogen
from typing import Dict, List
from autogen import ConversableAgent
import sys
import os

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    reviews = []
    # TODO
    try:
        with open("restaurant-data.txt", "r") as file:
            for line in file:
                # Remove leading/trailing whitespace
                line = line.strip()
                # Check if line starts with the restaurant name (case insensitive)
                if line.lower().startswith(restaurant_name.lower()):
                    # Extract the review part after the restaurant name and period
                    review = line[len(restaurant_name):].strip()
                    # Remove the leading period and space if they exist
                    if review.startswith('.'):
                        review = review[1:].strip()
                    reviews.append(review)
        
        return {restaurant_name: reviews}
    except FileNotFoundError:
        print("Error: restaurant-reviews.txt file not found")
        return {restaurant_name: []}

    # This function takes in a restaurant name and returns the reviews for that restaurant. 
    # The output should be a dictionary with the key being the restaurant name and the value being a list of reviews for that restaurant.
    # The "data fetch agent" should have access to this function signature, and it should be able to suggest this as a function call. 
    # Example:
    # > fetch_restaurant_data("Applebee's")
    # {"Applebee's": ["The food at Applebee's was average, with nothing particularly standing out.", ...]}
    pass


def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    import math
    
    # Ensure both lists have same length
    N = len(food_scores)
    if N != len(customer_service_scores):
        raise ValueError("Food scores and customer service scores must have same length")
    
    total_score = 0
    
    # Calculate score using the provided formula
    for i in range(N):
        # sqrt(food_scores[i]**2 * customer_service_scores[i])
        term = math.sqrt(food_scores[i]**2 * customer_service_scores[i])
        
        # Multiply by 1/(N * sqrt(125)) * 10
        term = term * (1 / (N * math.sqrt(125))) * 10
        
        total_score += term
    
    # Return with at least 3 decimal places as per requirements
    return {restaurant_name: round(total_score, 3)}

    # TODO

    
    # This function takes in a restaurant name, a list of food scores from 1-5, and a list of customer service scores from 1-5
    # The output should be a score between 0 and 10, which is computed as the following:
    # SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    # The above formula is a geometric mean of the scores, which penalizes food quality more than customer service. 
    # Example:
    # > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    # {"Applebee's": 5.048}
    # NOTE: be sure to that the score includes AT LEAST 3  decimal places. The public tests will only read scores that have 
    # at least 3 decimal places.
  
def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
     prompt = f"""Given the user query: "{restaurant_query}"

        Your task is to:
        1. Identify and extract the restaurant name from the query
        2. Suggest calling the fetch_restaurant_data function with the extracted restaurant name
        3. Be precise with restaurant name extraction, maintaining proper capitalization

        Example formats of queries you might receive:
        - "How good is McDonald's as a restaurant"
        - "What would you rate In N Out?"
        - "Tell me about Subway"

        Please analyze the query and suggest the appropriate function call with the correct restaurant name.

        Query to analyze: {restaurant_query}"""

     return prompt
    
    # TODO
    # It may help to organize messages/prompts within a function which returns a string. 
    # For example, you could use this function to return a prompt for the data fetch agent 
    # to use to fetch reviews for a specific restaurant.
    

# TODO: feel free to write as many additional functions as you'd like.

# Do not modify the signature of the "main" function.
def main(user_query: str):
    # Create system message for entrypoint agent
    entrypoint_agent_system_message = """You are a supervisor agent that coordinates restaurant review analysis.
    Your tasks:
    1. Coordinate with the data fetch agent to get restaurant reviews
    2. Pass reviews to the analysis agent for scoring
    3. Ensure final scores are calculated correctly
    4. Manage the flow of information between agents"""
    
    # LLM config (using gpt-4-mini as recommended)
    llm_config = {
        "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]
    }
    
    # Create entrypoint agent
    entrypoint_agent = ConversableAgent(
        "entrypoint_agent",
        system_message=entrypoint_agent_system_message,
        llm_config=llm_config
    )
    
    # Register the fetch function
    entrypoint_agent.register_for_llm(
        name="fetch_restaurant_data",
        description="Fetches the reviews for a specific restaurant."
    )(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(
        name="fetch_restaurant_data"
    )(fetch_restaurant_data)
    
    # Create data fetch agent
    data_fetch_agent = ConversableAgent(
        "data_fetch_agent",
        system_message=get_data_fetch_agent_prompt(user_query),
        llm_config=llm_config
    )
    
    # Create review analyzer agent
    review_analyzer_agent = ConversableAgent(
        "review_analyzer_agent",
        system_message="""You analyze restaurant reviews and extract scores based on specific keywords:
        Food Scores (1-5):
        - 1: awful, horrible, disgusting
        - 2: bad, unpleasant, offensive
        - 3: average, uninspiring, forgettable
        - 4: good, enjoyable, satisfying
        - 5: awesome, incredible, amazing
        
        Service Scores (1-5): Use same keywords
        
        Extract both food and service scores from each review.""",
        llm_config=llm_config
    )
    
    # Create scoring agent
    scoring_agent = ConversableAgent(
        "scoring_agent",
        system_message="""You take the analyzed reviews with their food and service scores and:
        1. Collect all food scores and service scores
        2. Call calculate_overall_score with these scores
        3. Return the final score""",
        llm_config=llm_config
    )
    
    # Initiate sequential chats
    result = entrypoint_agent.initiate_chats([
        {
            "recipient": data_fetch_agent,
            "message": f"User query: {user_query}. Please help extract the restaurant name and fetch reviews.",
            "summary_method": "last_message",
            "max_consecutive_auto_reply": 3
        },
        {
            "recipient": review_analyzer_agent,
            "message": "Please analyze these reviews and extract food and service scores.",
            "summary_method": "last_message",
            "max_consecutive_auto_reply": 3
        },
        {
            "recipient": scoring_agent,
            "message": "Please calculate the final score using the extracted scores.",
            "summary_method": "last_message",
            "max_consecutive_auto_reply": 3
        }
    ])
    
# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "review the subway resturaunt."
    main(sys.argv[1])