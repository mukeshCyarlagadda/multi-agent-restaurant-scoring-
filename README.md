# Restaurant Review Analysis System

## Overview

This project uses AutoGen to create a multi-agent workflow that analyzes unstructured restaurant reviews and provides quantitative scores for restaurants based on qualitative text reviews.

The system processes natural language queries about restaurants (e.g., "How good is Subway?") and returns a numerical score based on the reviews contained in the dataset.

## Architecture

The solution follows a sequential multi-agent architecture with the following components:

- **Entry Point Agent**: Coordinates the overall workflow and manages communication between other agents
- **Data Fetch Agent**: Extracts the restaurant name from the query and suggests fetching data for that restaurant
- **Review Analysis Agent**: Analyzes the fetched restaurant reviews and extracts food and service scores
- **Scoring Agent**: Takes the extracted scores and calculates the final overall score
  
![image](https://github.com/user-attachments/assets/b37727ed-8343-4aaf-9950-91bf674c73d8)

The workflow proceeds as follows:

1. Extract the restaurant name from the query
2. Fetch relevant reviews for the specified restaurant
3. Analyze the reviews to extract scores for food quality and customer service
4. Calculate an overall score for the restaurant

## Scoring System

The system analyzes reviews based on specific keywords:

### Score Keywords
- **Score 1/5**: awful, horrible, disgusting
- **Score 2/5**: bad, unpleasant, offensive
- **Score 3/5**: average, uninspiring, forgettable
- **Score 4/5**: good, enjoyable, satisfying
- **Score 5/5**: awesome, incredible, amazing

Each review is analyzed to extract:
- `food_score`: Quality of food (1-5)
- `customer_service_score`: Quality of service (1-5)

The final score is calculated using a geometric mean formula that weights food quality higher than customer service.

## Implementation Details

### Key Files
- `main.py`: Contains the main implementation of the multi-agent workflow
- `restaurant-data.txt`: Dataset containing restaurant reviews
- `test.py`: Test cases for validating the system's performance

### Functions
- `fetch_restaurant_data()`: Extracts reviews for a specific restaurant
- `calculate_overall_score()`: Computes the overall restaurant score using the formula:
SUM(sqrt(food_scores[i]^2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10)

## Setup and Usage

### Requirements
The project requires several Python packages, all listed in `requirements.txt`. Key dependencies include:
- AutoGen
- OpenAI API





