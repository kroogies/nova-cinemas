import requests
from flask import Flask, render_template, request
import mysql.connector
from flask import session
import os
from datetime import timedelta

connection = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="minimumM4.", 
    database="novacinemas"
)

db = connection.cursor()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
app.permanent_session_lifetime = timedelta(days=1)

# Replace with your actual token
bearer_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkMzA0MGVmYWJmNDU3YWViNTNmMWQ3OGQ5OWQyZjdhYyIsIm5iZiI6MTcyOTc3MzcyMi45OTAyNzUsInN1YiI6IjY3MWEzZTJhNWJlOWU4NzU5ZGE2ZjEwNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.r_ire39scdLKtpyTIfxCv2KOo3AZDUr4N7WTNMXnCdw'

# Define date range
min_date = '2024-11-01'
max_date = '2024-12-29'

# Define the base URL for movie poster images
image_base_url = 'https://image.tmdb.org/t/p/w500'

# Initialize the list to store all movie data
all_movies = []

# Fetch movie data
total_pages = 1  # Start with the first page
for page in range(1, total_pages + 1):
    url = f'https://api.themoviedb.org/3/movie/now_playing?language=en-US&page={page}&region=PH'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        page_data = response.json()
        all_movies.extend(page_data['results'])
        
        # Update total_pages based on the first response
        if page == 1:
            total_pages = page_data['total_pages']
    else:
        print(f"Failed to retrieve data for page {page}: {response.status_code} - {response.text}")

# Filter movies by date and prepare data for the template
filtered_movies = []

for movie in all_movies:
    release_date = movie['release_date']
    if min_date <= release_date <= max_date:
        title = movie['title']
        poster_path = movie['poster_path']
        if poster_path:
            poster_url = f"{image_base_url}{poster_path}"

            filtered_movies.append({
                'title': title,
                'release_date': release_date,
                'poster_url': poster_url
            })
filtered_movies = filtered_movies[:16]

#######################################################
# Define the date range for "Coming Soon" movies
min_date_coming_soon = '2024-12-20'  # Start of coming soon range
max_date_coming_soon = '2025-02-28'  # End of coming soon range

# Fetch "Coming Soon" movies from the "upcoming" endpoint
total_pages_upcoming = 1
coming_soon_movies = []

for page in range(1, total_pages_upcoming + 1):
    url = f'https://api.themoviedb.org/3/movie/upcoming?language=en-US&page={page}&region=PH'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'accept': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        page_data = response.json()
        if page == 1:
            total_pages_upcoming = page_data['total_pages']  # Update total pages on the first request

        for movie in page_data['results']:
            release_date = movie.get('release_date')
            if release_date and min_date_coming_soon <= release_date <= max_date_coming_soon:
                title = movie.get('title')
                poster_path = movie.get('poster_path')
                poster_url = f"{image_base_url}{poster_path}" if poster_path else None

                coming_soon_movies.append({
                    'title': title,
                    'release_date': release_date,
                    'poster_url': poster_url
                })
    else:
        print(f"Failed to fetch data for page {page}: {response.status_code} - {response.text}")

@app.route('/')
def home():
    return render_template('index.html', now_playing=filtered_movies, coming_soon=coming_soon_movies)

@app.route('/<movie_slug>')
def movie_details(movie_slug):
    movie_name = movie_slug.replace("-", " ").title()

    # Store the movie_slug and movie_name in session
    session['movie_slug'] = movie_slug
    session['movie_name'] = movie_name

    # Search for the movie in TMDb API
    url = f'https://api.themoviedb.org/3/search/movie?query={movie_name}&language=en-US'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'accept': 'application/json',
    }
    response = requests.get(url, headers=headers)

    movie_description = None
    poster_url = None
    trailer_url = None  # Initialize the trailer URL

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie = data['results'][0]  # Get the first search result
            movie_description = movie.get('overview', 'No description available.')
            poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None

            # Fetch the trailer URL
            movie_id = movie['id']
            video_url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US'
            video_response = requests.get(video_url, headers={'Authorization': f'Bearer {bearer_token}'})
            if video_response.status_code == 200:
                video_data = video_response.json()
                if video_data['results']:
                    trailer_url = video_data['results'][0]['key']  # Get the first trailer key

    # Fetch movie_id from the database based on movie name
    movie_id_result = db.execute("SELECT id FROM movies WHERE title = %s", (movie_name,))
    movie_id_result = db.fetchone()

    if movie_id_result:
        movie_id = movie_id_result[0]
        # Fetch showtimes for the movie
        showtimes_result = db.execute("SELECT showtime FROM showtimes WHERE movie_id = %s", (movie_id,))
        showtimes_result = db.fetchall()
        showtimes = [showtime[0] for showtime in showtimes_result]
        formatted_showtimes = ', '.join(showtimes)

        cinema_id_result = db.execute("SELECT cinema_id FROM showtimes WHERE movie_id = %s", (movie_id,))
        cinema_id_result = db.fetchone()
        cinema_id = cinema_id_result[0]
    else:
        formatted_showtimes = []
        cinema_id = None  # Add this to handle cases where cinema_id is not available

    # Store formatted_showtimes and cinema_id in session
    session['formatted_showtimes'] = formatted_showtimes
    session['cinema_id'] = cinema_id

    return render_template('checkout.html', movie_name=movie_name, description=movie_description, 
                           poster_url=poster_url, trailer_url=trailer_url, 
                           showtimes=formatted_showtimes, cinema_id=cinema_id)

@app.route('/<movie_slug>/checkout', methods=['GET', 'POST'])
def movie_checkout(movie_slug):
    # Retrieve movie_slug and movie_name from session
    movie_slug = session.get('movie_slug')
    movie_name = session.get('movie_name')
    formatted_showtimes = session.get('formatted_showtimes', [])
    cinema_id = session.get('cinema_id', None)

    if not cinema_id:
        return "Cinema not found!", 404

    # Fetch seats for the given cinema_id from the database
    query = """
    SELECT id, row_num, column_letter, is_booked
    FROM seats
    WHERE cinema_id = %s
    ORDER BY row_num, column_letter
    """
    db.execute(query, (cinema_id,))
    seats_result = db.fetchall()

    # Organize the seat data into a more user-friendly structure
    seats = {}
    for seat in seats_result:
        seat_id = seat[0]
        row = seat[1]
        column = seat[2]
        is_booked = seat[3]
        if row not in seats:
            seats[row] = {}
        seats[row][column] = {'seat_id': seat_id, 'is_booked': is_booked}

    if request.method == 'POST':
        # Handle seat selection when form is submitted
        selected_seats = request.form.getlist('selected_seats')

        if selected_seats:
            # Mark the selected seats as booked in the database
            try:
                for seat_id in selected_seats:
                    query = "UPDATE seats SET is_booked = 1 WHERE seat_id = %s"
                    db.execute(query, (seat_id,))

                # Commit the transaction
                connection.commit()

                return render_template('forms.html', seats=selected_seats)
            except Exception as e:
                connection.rollback()
                return f"Error occurred: {str(e)}", 500

    return render_template('forms.html', movie_slug=movie_slug, movie_name=movie_name, 
                           showtimes=formatted_showtimes, cinema_id=cinema_id, seats=seats)

if __name__ == '__main__':
    app.run(debug=True)
