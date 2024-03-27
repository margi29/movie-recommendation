from flask import Flask, render_template
import csv
from datetime import datetime
app = Flask(__name__)

# Function to fetch details for 15 movies from the dataset
def fetch_top_movies():
    top_movies = []
    trending_movies = []
    popular_movies = []

    with open('dataset/new_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie_detail = {
                'backdrop_path': "https://image.tmdb.org/t/p/w1280/" + row['backdrop_path'],
                'poster_path': "https://image.tmdb.org/t/p/w1280/" + row['poster_path'],
                'title': row['title'],
                'release_date': row['release_date'],
                'runtime': row['runtime'],
                'vote_average': row['vote_average'],
                'certification': row['certification'],
                'genres': row['genres'],
                'overview': row['overview'],
                'casts': row['casts'],
                'directors': row['directors'],
                'keywords': row['keywords']
            }
            add_videos(movie_detail, row['videos'])
            top_movies.append(movie_detail)

            # Check if the movie is trending
            if float(row['vote_average']) > 7.5:
                trending_movies.append(movie_detail)

            # Check if the movie is popular (released in the current year with rating above 8.0)
            if float(row['vote_average']) > 8.5:
                popular_movies.append(movie_detail)

            # Break the loop if 15 eligible movies are found
            if len(top_movies) == 50 and len(trending_movies) >= 5 and len(popular_movies) >= 5:
                break

    return top_movies[:15], trending_movies[:15], popular_movies[:15]  # Return only the top 5 trending and popular movies

# Function to add videos to the movie details dictionary
def add_videos(movie_detail, videos):
    video_urls = videos.split(', ')  # Assuming videos are separated by commas in the CSV
    movie_detail['videos'] = ["https://www.youtube.com/embed/" + url + "?&theme=dark&color=white&rel=0" for url in video_urls]

# Route for rendering the index page with top 15 movies
@app.route('/')
def index():
    top_movies, trending_movies, popular_movies = fetch_top_movies()
    return render_template('index.html', movies=top_movies, trending=trending_movies, popular=popular_movies)

@app.route('/detail')
def detail():
    top_movies, _, _ = fetch_top_movies()  # Only fetching top movies for detail page
    return render_template('detail.html', movies=top_movies)

@app.route('/movie-list')
def movie_list():
    top_movies, _, _ = fetch_top_movies()  # Only fetching top movies for movie list page
    return render_template('movie-list.html', movies=top_movies)

if __name__ == '__main__':
    app.run(debug=True)
