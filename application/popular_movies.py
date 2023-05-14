import requests

def get_popular_movies():
    # Replace 'YOUR_API_KEY' with your actual OMDB API key
    api_key = '374c6e5b'
    
    # API request URL to fetch popular movies
    url = f'http://www.omdbapi.com/?apikey={api_key}&s=&type=movie&r=json'
    
    try:
        # Send GET request to OMDB API
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the movie data from the response
            data = response.json()
            
            # Check if the response contains movie results
            if data['Response'] == 'True':
                # Extract the movie list
                movies = data['Search']
                
                print(movies)
                # Return the list of movies as JSON
                # return jsonify(movies)
                return movies
            
        # If the request was not successful, return an error message
        # return jsonify({'message': 'Failed to fetch popular movies'})
    
    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the request
        # return jsonify({'message': 'An error occurred: {}'.format(e)})
        return None
    

print(get_popular_movies())
