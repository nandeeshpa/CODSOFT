import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#  Load dataset
try:
    movies = pd.read_csv('movies.csv')
except FileNotFoundError:
    print("❌ Error: movies.csv not found.")
    exit()

#  Handle missing data
movies['genres'] = movies['genres'].fillna('')
tfidf = TfidfVectorizer(token_pattern=r'\b[a-zA-Z]{1,}\b', stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#  Title Index Mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

#  Recommendation Function
def recommend(title, num_recommendations=5):
    if title not in indices:
        return f"❌ Movie '{title}' not found in the dataset."
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

#  Start Program
print("🎬 Welcome to the Movie Recommendation System!")

while True:
    print("\n📄 Available Movies:")
    for i, title in enumerate(movies['title'], 1):
        print(f"{i}. {title}")

    user_input = input("\nEnter a movie title exactly as shown above: ")

    result = recommend(user_input)
    print(f"\n🎯 People who watched '{user_input}' also liked:")
    if isinstance(result, str):
        print(result)
    else:
        for i, title in enumerate(result, 1):
            print(f"{i}. {title}")

    again = input("\n🔁 Do you want to search for another movie? (yes/no): ").strip().lower()
    if again not in ['yes', 'y']:
        print("\n👋 Thanks for using the Movie Recommendation System! Goodbye.")
        break
