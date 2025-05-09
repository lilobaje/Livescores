from flask import Flask, render_template, jsonify, send_from_directory
import requests
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Config
API_KEY = os.environ.get("API_KEY", "")  # Get API key from environment variables
SPORT = "football"  # You can change this to basketball, cricket, etc.

# Cache for storing the latest data
# In a production app, you might want to use Redis or another caching solution
score_cache = {
    "last_updated": None,
    "matches": []
}

def fetch_live_scores():
    """Fetch live scores from the API"""
    try:
        # Using API-Football as an example
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

@app.route('/')
def index():
    # For Vercel deployment, we need to use a different approach for templates
    return render_template('index.html')

@app.route('/api/scores')
def get_scores():
    """API endpoint to get the latest scores"""
    # Try to fetch fresh scores first (for serverless environment)
    if API_KEY:
        fetch_live_scores()
    
    # If we have no scores or API key, use mock data
    if not score_cache["matches"] or not API_KEY:
        return get_mock_scores()
    
    return jsonify(score_cache)

@app.route('/api/mock-scores')
def get_mock_scores():
    """API endpoint to get mock scores for testing"""
    mock_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "matches": [
            {
                "id": 1,
                "home_team": "Manchester United",
                "away_team": "Liverpool",
                "home_score": 2,
                "away_score": 1,
                "elapsed": 75,
                "league": "Premier League",
                "country": "England"
            },
            {
                "id": 2,
                "home_team": "Barcelona",
                "away_team": "Real Madrid",
                "home_score": 0,
                "away_score": 0,
                "elapsed": 32,
                "league": "La Liga",
                "country": "Spain"
            },
            {
                "id": 3,
                "home_team": "Bayern Munich",
                "away_team": "Borussia Dortmund",
                "home_score": 3,
                "away_score": 1,
                "elapsed": 65,
                "league": "Bundesliga",
                "country": "Germany"
            },
            {
                "id": 4,
                "home_team": "Paris Saint-Germain",
                "away_team": "Marseille",
                "home_score": 1,
                "away_score": 0,
                "elapsed": 42,
                "league": "Ligue 1",
                "country": "France"
            },
            {
                "id": 5,
                "home_team": "AC Milan",
                "away_team": "Inter Milan",
                "home_score": 1,
                "away_score": 2,
                "elapsed": 84,
                "league": "Serie A",
                "country": "Italy"
            }
        ]
    }
    return jsonify(mock_data)

# Special path for templates in Vercel
@app.route('/templates/<path:path>')
def send_template(path):
    return send_from_directory('templates', path)

# Make templates directory available
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')