import argparse
import json
import os
import difflib
from RapidAPI_6 import search_movies

"""
This script is for me to practice the use case of api using rapidAPI to search movies
print to the client the rquested movies using argparse
reduce API calls using json file that keep the data
"""

# נתיב לקובץ ה-JSON
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(script_dir, 'movies.json')

def load_json():
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        try:
            with open(json_file, 'r') as infile:
                return json.load(infile)
        except json.JSONDecodeError:
            print("JSON is invalid. Starting fresh.")
    return {}

def save_json(data):
    with open(json_file, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def print_movies(movies):
    for movie in movies:
        print(f"Title: {movie['Title']}, Year: {movie['Year']}")

def main():
    parser = argparse.ArgumentParser(description='search for a pattern in the movie database')
    parser.add_argument('pattern', help='the movie title to search')
    args = parser.parse_args()
    pattern = args.pattern.lower()
    print(f'searching for pattern: {pattern}')
    data = load_json()
    
    if pattern in data:
        print("Found in cache:")
        print_movies(data[pattern])
        return

    similar_keys = difflib.get_close_matches(pattern, data.keys(), n=1)
    if similar_keys:
        print(f"No exact match. Did you mean '{similar_keys[0]}'?")
        print_movies(data[similar_keys[0]])
        return
    
    print("Fetching from API...")
    response = search_movies(pattern)
    if response.status_code == 200:
        result = response.json()
        if "Search" in result:
            data[pattern] = result["Search"]
            save_json(data)
            print("Results:")
            print_movies(result["Search"])
        else:
            print("No movies found in API.")
    else:
        print(f"API request failed. Status: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
