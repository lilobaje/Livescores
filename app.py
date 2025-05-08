from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime
import time
import threading

app = Flask(__name__)

# Config
API_KEY = "22024e49a88d83491361bf61dc780a94"  # Replace with your API key
SPORT = "football"  # You can change this to basketball, cricket, etc.

# Cache for storing the latest data
score_cache = {
    "last_updated": None,
    "matches": []
}

def fetch_live_scores():
    """Fetch live scores from the API"""
    try:
        # Using API-Football as an example (you'll need to sign up for a key)
        url = f"https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            matches = []
            
            # Parse the data according to the API's structure
            if "response" in data:
                for match in data["response"]:
                    match_data = {
                        "id": match["fixture"]["id"],
                        "home_team": match["teams"]["home"]["name"],
                        "away_team": match["teams"]["away"]["name"],
                        "home_score": match["goals"]["home"],
                        "away_score": match["goals"]["away"],
                        "elapsed": match["fixture"]["status"]["elapsed"],
                        "league": match["league"]["name"],
                        "country": match["league"]["country"]
                    }
                    matches.append(match_data)
            
            # Update the cache
            score_cache["matches"] = matches
            score_cache["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return True
        else:
            print(f"API request failed with status code: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Error fetching scores: {str(e)}")
        return False

def update_scores_periodically():
    """Background thread to update scores every minute"""
    while True:
        print("Updating scores...")
        fetch_live_scores()
        time.sleep(60)  # Update every 60 seconds

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/scores')
def get_scores():
    """API endpoint to get the latest scores"""
    return jsonify(score_cache)

if __name__ == '__main__':
    # Start the background thread for updating scores
    if API_KEY != "YOUR_API_KEY_HERE":  # Only start if API key is provided
        score_thread = threading.Thread(target=update_scores_periodically)
        score_thread.daemon = True
        score_thread.start()
    
    # For development
    app.run(debug=True)