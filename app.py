import sys
import numpy as np
from flask import Flask, render_template, request, url_for, redirect
from pickle import load

########## additional code for unzip "similarity_scores.bin" file ##########
if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

zip_ref = zipfile.ZipFile("model/similarity_scores.zip", "r")
zip_ref.extractall("model/")
zip_ref.close()
############################################################################


app = Flask(__name__)


## database/ dataframe loading...
movies_df = load(open("model/movies_df.bin", "rb"))
popular_movies = load(open("model/popular_movies.bin", "rb"))
final_train_df = load(open("model/final_train_df.bin", "rb"))
similarity_scores = load(open("model/similarity_scores.bin", "rb"))



## search suggestions...randomly choosen..
movies = movies_df["title"].unique()
search_suggestions_idx = list(movies[np.random.randint(0, len(movies), 20)])
search_suggestions = list(map(lambda x : x.title(), search_suggestions_idx))



## Poster Link getting function:

def get_poster_link(tmdbID):
  req = requests.get(f"http://api.themoviedb.org/3/movie/{tmdbID}?api_key=8265bd1679663a7ea12ac168da84d2e8")                   ## API link
  
  if req.status_code == 200:
    poster_path = str(req.json()["poster_path"])
  else:
    poster_path = ""

  return f"http://image.tmdb.org/t/p/w185{poster_path}"   



@app.route("/")
def index():
    top_15 = popular_movies.iloc[:150, ].copy()
    top_15["title"] = top_15["title"].apply(lambda x : x.title())
    img_links = top_15["img_link"].values.tolist()
    movie_names = top_15["title"].values.tolist()
    runtimes = top_15["runtime"].values.tolist()
    popularity = top_15["popularity"].values.tolist()
    avg_rating = top_15["vote_average"].values.tolist()
    status = top_15["status"].values.tolist()
    release_date = top_15["release_date"].values.tolist()

    return render_template("index.html", img_links=img_links, movie_names=movie_names, runtimes=runtimes, status=status, avg_rating=avg_rating, popularity=popularity, release_date=release_date)



@app.route("/recommend")
def recommend_load_ui():
    
    return render_template("recommendation.html", search_suggestions=search_suggestions)


@app.route("/recommend_movies", methods=["POST"])
def recommend():
    usr_input = str(request.form.get("usr_input")).lower().split()
    movie_name = " ".join(usr_input)
    output = "Recommended Movies"
    datas = []

    try:
        idx = np.where(final_train_df["title"] == movie_name)[0][0]

        indices = sorted(enumerate(similarity_scores[idx]), reverse=True, key=lambda x : x[1])[1:7]
        most_similar_idx = list(map(lambda x : x[0], indices))

        similar_movies = list(final_train_df.iloc[most_similar_idx, ]["title"])

        for movie in similar_movies:
            mv_df = movies_df.loc[movies_df["title"] == movie]
            mv_datas = [mv_df["title"].values[0].title(), get_poster_link(mv_df["tmdbId"].values[0]), mv_df["runtime"].values[0], mv_df["vote_average"].values[0], mv_df["release_date"].values[0], mv_df["status"].values[0]]
            datas.append(mv_datas)
    except:
        output = False
        datas = "Sorry, Movie Not Found!"

    return render_template("recommendation.html", datas=datas, output=output, search_suggestions=search_suggestions)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


## Feedback transmission system via mail.. ;)
def feedback_mail(message):
    import smtplib
    from datetime import datetime

    message = message + "\nUTC time: " + datetime.isoformat(datetime.utcnow())
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("feedbackmovierecommender@gmail.com", "suixoyqcouckzhvi")
    s.sendmail("feedbackmovierecommender@gmail.com", "deltagon@protonmail.com", message)
    s.quit()


@app.route('/6810c3c04069ca9707728937d86239a66ca346e8', methods=['POST'])
def fetch_feedback():
    name = str(request.form.get('name'))
    email = str(request.form.get('email'))
    message = str(request.form.get('message'))

    if len(name) > 0 or len(email) > 0 or len(message) > 0:
        feedback_mail(f"[Movie Recommender Feedback Bot]\nName- {name}\nMail- {email}\nFeedback- {message}")             ## Optimization - to save server computational power

        return render_template('contact.html', tnx_feedback="Thank you for feedback!")
    return redirect(url_for('contact'))



if __name__ == "__main__":
    app.run(debug=True)
