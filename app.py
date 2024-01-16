from flask import Flask, render_template, request, redirect
import csv
from pathlib import Path
from flask import send_file

app = Flask(__name__)

csv_file_path = r"./movies_metadata.csv"

movies_data = []
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        movies_data.append(row)


# Function to search for movies locally
def search_movies_local(query):
    return [movie for movie in movies_data if query.lower() in movie.get('original_title', '').lower()]


# Function to delete a movie locally by original title
def delete_movie_local(movie_id):
    global movies_data  # Ensure we're modifying the global variable
    movies_data = [movie for movie in movies_data if movie.get('id', '').lower() != str(movie_id).lower()]


# Function to update a movie locally
# Function to update a movie locally
def update_movie_local(movie_id, data):
    for movie in movies_data:
        if movie['id'] == movie_id:
            movie.update(data)
            break  # Stop iterating once the movie is updated


# Home Page
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        query = request.form.get('query', '')
        result = search_movies_local(query)
        return render_template('index.html', movies_data=result)
    return render_template('index.html', movies_data=None)


# Update Page
@app.route('/update/<original_title>', methods=['GET', 'POST'])
def update(original_title):
    movie_info = next((movie for movie in movies_data if movie['original_title'].lower() == original_title.lower()),
                      None)

    if request.method == 'POST':
        update_data = {}
        for field in ['adult', 'belongs_to_collection', 'budget', 'original_language', 'original_title', 'revenue',
                      'production_countries', 'release_date',
                      'vote_average', 'popularity', 'genres', 'title', 'overview', 'id', 'vote_count',
                      'homepage', 'status', 'production_companies', 'imdb_id', 'tagline', 'video', 'poster_path',
                      'spoken_languages', 'runtime']:
            update_data[field] = request.form.get(field, movie_info.get(field, ''))
        # Update the movie using the actual movie ID
        update_movie_local(movie_info['id'], update_data)
        return redirect('/')

    return render_template('update.html', movie=movie_info)


# Info Page
@app.route('/info/<movie_name>', methods=['GET'])
def info(movie_name):
    movie_info = next((movie for movie in movies_data if movie['original_title'].lower() == movie_name.lower()), None)

    if movie_info:
        return render_template('info.html', movie_info=movie_info)
    else:
        return render_template('info.html', movie_info=None, message="Movie not found")


# Add Movie Page
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        new_movie_data = {}
        for field in ['adult', 'belongs_to_collection', 'budget', 'original_language', 'original_title', 'revenue',
                      'production_countries', 'release_date',
                      'vote_average', 'popularity', 'genres', 'title', 'overview', 'id', 'vote_count',
                      'homepage', 'status', 'production_companies', 'imdb_id', 'tagline', 'video', 'poster_path',
                      'spoken_languages', 'runtime']:
            new_movie_data[field] = request.form.get(field, '')
        # Generate a unique ID for the new movie (replace this with your logic)
        new_movie_data['id'] = len(movies_data) + 1
        movies_data.append(new_movie_data)
        return redirect('/')
    return render_template('addmovie.html')


# deletes movie
@app.route('/delete/<int:movie_id>', methods=['GET'])
def delete(movie_id):
    delete_movie_local(movie_id)
    return redirect('/')


@app.route('/download_csv', methods=['GET'])
def download_csv():
    # Save the changes to a new CSV file
    new_csv_file_path = csv_file_path.replace('.csv', '_updated.csv')
    with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = movies_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies_data)

    # Return the new file for download
    return send_file(new_csv_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
