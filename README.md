# Movie Recommender AI System

This is a movie recommender AI system that uses a content-based approach to recommend similar movies to the user. It generates a tagline for each movie using its overview text, genres, keywords, cast characters info, and director name. Then, it uses cosine similarity to calculate the similarity score between the movies based on their taglines and recommends the 7 closest movies holding the largest cosine similarity scores.

## Dataset

The dataset used for this project is the [TMDB movie metadata dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset), which contains information about over 5000 movies, including their titles, overview texts, genres, keywords, cast characters info, and director names.

## Description

In addition to the features provided in the dataset, this movie recommender AI system also collects the movie poster link using the movie's TmdbId from the [TMDB API](https://www.themoviedb.org/documentation/api), which is used to display the movie poster in the recommendation results.

## Usage

To use this movie recommender AI system, simply provide the title of a movie as input, and it will recommend 8 similar movies based on the movie's features. You can adjust the number of recommended movies by changing the value in the code.

## License

This project is licensed under the [MIT License](https://github.com/ishtiuk/Movie-Recommender-AI/blob/main/LICENSE).

## Credits

This movie recommender AI system was developed by [Md. Ishtiuk Ahammed](https://github.com/ishtiuk). Special thanks to the creators of the [TMDB movie metadata dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) and [TMDB API](https://www.themoviedb.org/documentation/api) for providing the data and movie poster links, respectively.


```python
# Example usage.

moviename = "the avengers"
print("\n\n[RECOMMENDATIONS]\n")

for movie_data in recommender_engine(moviename):
  print(movie_data)
  
