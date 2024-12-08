from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd


# Simulating the hybrid recommendations 
hybrid_recommendations = pd.DataFrame({
    'id': [151, 161, 159, 560, 540, 44, 31, 549, 173, 129],
    'title': ['unknown', 'unknown', 'unknown', 'unknown', 'unknown', 'escape the matrix', "Don't laugh", 'unknown', 'unknown', 'unknown'],
    'category': [
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}',
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}',
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}', 
        '{"id": 2, "name": "Vible", "count": 534, "description": "All the best vibes!"}'
    ],
    'score': [12.0, 10.0, 9.0, 9.0, 8.0, 7.0, 6.0, 6.0, 4.0, 0.3],
    'source': ['collaborative', 'collaborative', 'collaborative', 'collaborative', 'collaborative', 
               'collaborative', 'collaborative', 'collaborative', 'collaborative', 'content']
})

# Simulated actual ratings (ground truth)
user_interactions_data = pd.DataFrame({
    'user_id': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3],
    'post_id': [151, 161, 159, 540, 560, 540, 549, 173, 149, 129],
    'rating_percent': [12, 10, 9, 8, 7, 6, 5, 6, 7, 0]  
})

def evaluate_recommendation(predictions, ground_truth):
    """
    Evaluate the recommendation system using MAE and RMSE.
    :param predictions: List of predicted ratings/interaction scores.
    :param ground_truth: List of actual ratings/interaction scores.
    :return: Dictionary containing MAE and RMSE values.
    """
    # Ensure both lists have the same length
    min_length = min(len(predictions), len(ground_truth))
    predictions = predictions[:min_length]
    ground_truth = ground_truth[:min_length]

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(ground_truth, predictions)
    
    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mean_squared_error(ground_truth, predictions))
    
    return {"MAE": mae, "RMSE": rmse}

def get_hybrid_predictions(hybrid_recommendations, top_n=10):
   
    # Get the top-N recommended videos
    top_recommendations = hybrid_recommendations.nlargest(top_n, 'score')

    # Extract predicted scores (scores represent predicted ratings)
    predicted_ratings = top_recommendations['score'].tolist()

    return predicted_ratings

def get_ground_truth(user_id, top_n=10):
    
    # Filter user interactions to get the ground truth (actual interactions/ratings)
    user_interactions = user_interactions_data[user_interactions_data['user_id'] == user_id]
    ground_truth = user_interactions['rating_percent'].head(top_n).tolist() 

    return ground_truth

# Example usage
if __name__ == "__main__":
    user_id = 1 
    top_n = 10 

    # Get predicted ratings from the hybrid recommendations
    predictions = get_hybrid_predictions(hybrid_recommendations, top_n)

    # Get the actual ratings (ground truth) for the user
    ground_truth = get_ground_truth(user_id, top_n)

    # Evaluate the recommendation algorithm
    metrics = evaluate_recommendation(predictions, ground_truth)

    # Print the evaluation metrics
    print(f"Evaluation Metrics: {metrics}")
