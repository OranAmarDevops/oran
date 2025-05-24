import requests

def search_movies(pattern):
    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {"s": pattern, "r": "json", "page" : "1"}
    headers = {
		"x-rapidapi-key": "7c41e491fdmsha522b68bf01bca9p148259jsn06fadbae9d0c",
		"x-rapidapi-host": "movie-database-alternative.p.rapidapi.com"
	}
    response = requests.get(url, headers=headers, params=querystring)
    return response