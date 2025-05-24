from flask import Flask, request ,render_template, jsonify, send_from_directory
import json
import os
import requests

search_file = 'search.json'
app = Flask(__name__)

# Initialize JSON file if it does not exist
if not os.path.exists(search_file):
    with open(search_file, "w") as f:
        json.dump({}, f)

@app.route('/', methods=['GET'])
def home():
    return render_template('main.html'), 200

@app.route('/<filename>', methods=['GET'])
def server_static(filename):
    allowed_extensions = ('.js', '.css', '.png', '.jpg', '.jpeg', '.gif')
    if filename.endswith(allowed_extensions):
        return send_from_directory('static', filename)
    return "Not Found", 404

@app.route('/get_movies', methods=['GET'])
def get_movies():
    search = request.args.get('search') 
    
    if not search:
        return jsonify({"Error": "Missing 'search' parameter"}), 400
    
    result = movie_search(search)
    return jsonify(result)  

@app.route('/health', methods=['GET'])
def check_health():
    return jsonify(status="ok")

def save_locally(search, data):
    """Save search result data locally."""
    with open(search_file, "r") as f:
        local_data = json.load(f)

    # Update with new search data
    local_data[search] = data

    with open(search_file, "w") as f:
        json.dump(local_data, f)

def load_locally(pattern):
    """Load search result data locally."""
    with open(search_file, "r") as f:
        return json.load(f).get(pattern)

def exists_locally(search):
    """Check if the search result exists locally."""
    with open(search_file, "r") as f:
        local_data = json.load(f)
        return search in local_data

def movie_search(pattern):
    """Search for movie data, retrieving from local storage if available."""
    # Check if data exists locally
    if exists_locally(pattern):
        return load_locally(pattern)
    
    # Fetch data from API if not found locally
    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {"s": pattern, "r": "json", "page": "1"}

    headers = {
        "x-rapidapi-key": "my_key",
        "x-rapidapi-host": "movie-database-alternative.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        api_resp = response.json()
        
        if 'Search' not in api_resp:
            return {"Error": "No results found in API response."}
        
        # Process and format API response
        result = {movie.get('Title', 'Unknown'): movie.get('Year', 'Unknown') for movie in api_resp['Search']}
        
        # Save API result locally
        save_locally(pattern, result)
        return result
    
    except requests.exceptions.RequestException as e:
        
        return {"Error": f"API request failed: {str(e)}"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
