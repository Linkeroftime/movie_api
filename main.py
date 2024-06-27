from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI

client = OpenAI(api_key='your-api-key')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    releaseYear = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    coverUrl = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(500), nullable=False)


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

def add_hardcoded_movies():
    if Movie.query.count() == 0:
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


 db.session.add(darkKnight)
        db.session.add(shawshankRedemption)
        db.session.commit()

@app.route('/getmovies', methods=['GET'])
def getMovies():
    movies = Movie.query.all()
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
    movies = Movie.query.filter_by(releaseYear=year).all()
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



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_hardcoded_movies()
    app.run(debug=True, host='0.0.0.0')


'''
TODO: add movie feature, web scraper functionality to get data from IMDB or otherwise, upload to cloud.
'''
