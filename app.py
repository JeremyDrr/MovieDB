from flask import Flask, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("https://4c0018bd50184c898d84a13014f88a5f.europe-west9.gcp.elastic-cloud.com:443",
                       api_key="cUVNQWRvMEJ4cmdBYl9qekZKVHA6R1dXQmVKekFTSTJ3NDRDWHo3T3g5UQ==")
# Function to retrieve all movies from ElasticSearch
def get_all_movies(query=None):
    if query:
        body = {
            "query": {
                "match": {
                    "Title": query
                }
            }
        }
        movies = es.search(index="moviesdb", body=body)["hits"]["hits"]
    else:
        movies = es.search(index="moviesdb", size=1000)["hits"]["hits"]
    return movies

# Function to retrieve a single movie by ID from ElasticSearch
def get_movie_by_id(movie_id):
    result = es.get(index="moviesdb", id=movie_id)
    return result["_source"]

# Function to add a new movie to ElasticSearch
def add_movie(movie_data):
    es.index(index="moviesdb", body=movie_data)

# Function to update an existing movie in ElasticSearch
def update_movie(movie_id, movie_data):
    es.index(index="moviesdb", id=movie_id, body=movie_data)

# Function to delete a movie from ElasticSearch
def delete_movie(movie_id):
    es.delete(index="moviesdb", id=movie_id)

# Display all movies
@app.route('/')
def index():
    query = request.args.get('query', '')
    movies = get_all_movies(query)
    return render_template('index.html', movies=movies, query=query)

# Display a single movie
@app.route('/movie/<movie_id>')
def get_movie(movie_id):
    movie = get_movie_by_id(movie_id)
    return render_template('movie.html', movie=movie)

# Add a new movie
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        movie_data = {
            "Title": request.form['Title'],
            "Genre": request.form['Genre'],
            "Description": request.form['Description'],
            "Director": request.form['Director'],
            "Actors": request.form['Actors'],
            "Year": request.form['Year'],
            "Runtime": request.form['Runtime'],
            "Rating": request.form['Rating'],
            "Votes": request.form['Votes'],
            "Revenue": request.form['Revenue'],
            "Metascore": request.form['Metascore']
        }

        # Retrieve the maximum rank currently in the database
        max_rank_query = {"aggs": {"max_rank": {"max": {"field": "Rank"}}}}
        max_rank_result = es.search(index="movies", body=max_rank_query)
        max_rank = max_rank_result["aggregations"]["max_rank"]["value"]

        # Assign rank to the new movie
        movie_data["Rank"] = max_rank + 1

        # Add the new movie to Elasticsearch
        add_movie(movie_data)

        return redirect(url_for('index'))
    return render_template('add.html')

# Update an existing movie
@app.route('/update/<movie_id>', methods=['GET', 'POST'])
def update(movie_id):
    if request.method == 'POST':
        movie_data = {
            "Title": request.form['Title'],
            "Genre": request.form['Genre'],
            "Description": request.form['Description'],
            "Director": request.form['Director'],
            "Actors": request.form['Actors'],
            "Year": request.form['Year'],
            "Runtime": request.form['Runtime'],
            "Rating": request.form['Rating'],
            "Votes": request.form['Votes'],
            "Revenue": request.form['Revenue'],
            "Metascore": request.form['Metascore']
        }
        update_movie(movie_id, movie_data)
        return redirect(url_for('index'))
    movie = get_movie_by_id(movie_id)
    return render_template('update.html', movie=movie)

# Delete a movie
@app.route('/delete/<movie_id>')
def delete(movie_id):
    delete_movie(movie_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
