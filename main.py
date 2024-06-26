from flask import Flask, jsonify
from openai import OpenAI

client = OpenAI(api_key='your-api-key')


app = Flask(__name__)

class Movie:
    def __init__(self, title, releaseYear, genre, coverUrl):
        self.title = title
        self.releaseYear = releaseYear
        self.genre = genre
        self.coverUrl = coverUrl
        self.summary = self.generate_summary()

    def generate_summary(self):
        prompt = f"Summarize the plot of the movie titled '{self.title}' in a concise paragraph."

        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the appropriate model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150)

        summary = response.choices[0].message.content.strip()
        return summary

darkKnight = Movie(
    "The Dark Knight", 
    2008, 
    "Action", 
    "https://irs.www.warnerbros.com/keyart-jpeg/movies/media/browser/the_dark_knight_key_art.jpg"
)



shawshankRedemption = Movie(
    "The Shawshank Redemption", 
    1994, 
    "Drama", 
    "https://www.imdb.com/title/tt0111161/mediaviewer/rm1690056449/?ref_=tt_ov_i"
)

movies = [darkKnight, shawshankRedemption]


@app.route('/getmovies', methods=['GET'])
def getMovies():
    movieData = []
    for movie in movies:
        movieData.append({
            "title":movie.title,
            "releaseYear":movie.releaseYear,
            "genre":movie.genre,
            "coverUrl":movie.coverUrl,
            "summary":movie.summary
        })
    return jsonify(movieData)

@app.route('/getmoviesbyyear/<int:year>', methods=['GET'])
def getMoviesByYear(year):
    movieData = []
    for movie in movies:
        if movie.releaseYear == year:
           movieData.append({
                "title":movie.title,
                "releaseYear":movie.releaseYear,
                "genre":movie.genre,
                "coverUrl":movie.coverUrl,
                "summary":movie.summary
            })
    return jsonify(movieData)



if __name__ == '__main__':
    app.run(debug=True)


'''
TODO: add movie feature, web scraper functionality to get data from IMDB or otherwise, upload to cloud.
'''
