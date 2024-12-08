from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Simulated data 
video_data = pd.DataFrame({
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

# Simulated hybrid recommendation function
def hybrid_recommendation(username, category_id=None, mood=None, top_n=10):
    recommendations = video_data
    
    #  filter based on category and mood
    if category_id:
        recommendations = recommendations[recommendations['category'].str.contains(str(category_id))]
    if mood:
        recommendations['score'] = recommendations['score'] * 1.1  
    
    return recommendations.nlargest(top_n, 'score')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feed', methods=['GET'])
def recommend_feed():
    username = request.args.get('username')
    category_id = request.args.get('category_id')
    mood = request.args.get('mood')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    recommendations = hybrid_recommendation(username, category_id, mood)

    return render_template('index.html', recommendations=recommendations.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
