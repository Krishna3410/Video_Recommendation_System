import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer


# Load Data
VIDEO_DATA_FILE = "processed_data/summary_posts.csv"  
USER_INTERACTIONS_FILE = "processed_data/viewed_posts.csv"  

video_data = pd.read_csv(VIDEO_DATA_FILE)
user_interactions = pd.read_csv(USER_INTERACTIONS_FILE)

# Content-Based Recommendation
def content_based_recommendation(username, category_id=None, top_n=10):
   
    # Filter user interactions
    user_history = user_interactions[user_interactions['user_id'] == username]

    # Check for missing columns and adjust feature extraction
    if 'tags' not in video_data.columns:
        print("Warning: 'tags' column is missing. Using 'category' and 'title' for feature extraction.")
        video_data['features'] = video_data['category'].fillna('') + " " + video_data['title'].fillna('')
    else:
        video_data['features'] = video_data['category'].fillna('') + " " + video_data['tags'].fillna('')

    # Convert text features into TF-IDF vectors
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(video_data['features'])

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # Get user's interacted video IDs
    user_video_ids = user_history['post_id'].unique()

    # Filter out already interacted videos
    unseen_videos = video_data[~video_data['id'].isin(user_video_ids)].copy()

    # Map similarity scores to unseen videos
    similarity_scores = similarity_matrix.mean(axis=1)
    unseen_videos['similarity_score'] = unseen_videos.index.map(
        lambda idx: similarity_scores[idx] if idx < len(similarity_scores) else 0
    )

    # Filter by category if provided
    if category_id:
        unseen_videos = unseen_videos[unseen_videos['category'] == category_id]

    # Return Top N recommendations
    return unseen_videos.nlargest(top_n, 'similarity_score')[['id', 'title', 'category', 'similarity_score']]


# Collaborative Filtering
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def collaborative_filtering(user_id, top_n=10):
    
    # Ensure the 'viewed_at' column exists
    if 'viewed_at' not in user_interactions.columns:
        raise KeyError("'viewed_at' column is missing in user_interactions data.")

    # Convert 'viewed_at' to a datetime format
    user_interactions['viewed_at'] = pd.to_datetime(user_interactions['viewed_at'])

    # Calculate the recency of interactions: more recent interactions are stronger
    max_date = user_interactions['viewed_at'].max()  # Latest date in the dataset
    user_interactions['interaction_strength'] = (max_date - user_interactions['viewed_at']).dt.days + 1

    # Create User-Item Interaction Matrix with interaction strength
    user_item_matrix = user_interactions.pivot_table(
        index='user_id', columns='post_id', values='interaction_strength', fill_value=0
    )

    # Compute User Similarity Matrix
    user_similarity = cosine_similarity(user_item_matrix)
    similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Find Similar Users (exclude the target user)
    similar_users = similarity_df[user_id].sort_values(ascending=False).index[1:]

    # Aggregate interaction strengths from similar users
    recommended_scores = user_item_matrix.loc[similar_users].mean(axis=0)

    # Filter out already interacted videos
    watched_videos = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index
    recommendations = recommended_scores[~recommended_scores.index.isin(watched_videos)]

    # Return Top N Recommendations
    top_recommendations = recommendations.nlargest(top_n)
    recommended_videos = video_data[video_data['id'].isin(top_recommendations.index)]

    return recommended_videos[['id', 'title', 'category', 'average_rating']]

# Hybrid Recommendation
def hybrid_recommendation(username, category_id=None, mood=None, top_n=10):
    
    # Get content-based recommendations
    content_recs = content_based_recommendation(username, category_id, top_n)
    content_recs['source'] = 'content'

    # Get collaborative filtering recommendations
    collaborative_recs = collaborative_filtering(username, top_n)
    collaborative_recs['source'] = 'collaborative'

    # Combine recommendations
    hybrid = pd.concat([content_recs, collaborative_recs]).drop_duplicates(subset='id', keep='first')

    # Average scores if available
    if 'similarity_score' in hybrid.columns and 'average_rating' in hybrid.columns:
        hybrid['score'] = hybrid[['similarity_score', 'average_rating']].mean(axis=1)
    elif 'similarity_score' in hybrid.columns:
        hybrid['score'] = hybrid['similarity_score']
    elif 'average_rating' in hybrid.columns:
        hybrid['score'] = hybrid['average_rating']

    # Return Top N recommendations
    return hybrid.nlargest(top_n, 'score')[['id', 'title', 'category', 'score', 'source']]

# Example Usage
if __name__ == "__main__":
    user_id = 1  
    category_id = None  
    mood = None  

    print("Content-Based Recommendations:")
    print(content_based_recommendation(user_id, category_id))

    print("\nCollaborative Filtering Recommendations:")
    print(collaborative_filtering(user_id))

    print("\nHybrid Recommendations:")
    print(hybrid_recommendation(user_id, category_id, mood))
