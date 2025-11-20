from textblob import TextBlob
import colorama
from colorama import Fore, Style
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import sys
import pandas as pd

colorama.init(autoreset=True)

def load_data(file_path = "imdb_top_1000.csv"):
    try:
        data = pd.read_csv(file_path)
        data["combined_features"] = data["Genre"].fillna('') + " " + data["Overview"].fillna('')
        return data
    except FileNotFoundError:
        print(Fore.RED + f"Data file not found. Please ensure '{file_path}' is in the working directory." + Style.RESET_ALL)
        exit()

movies_df = load_data()

tfdif = TfidfVectorizer(stop_words='english')
tfdif_matrix = tfdif.fit_transform(movies_df["combined_features"])
cosine_sim = cosine_similarity(tfdif_matrix, tfdif_matrix)

def list_genres(df):
    return sorted(set(genre.strip() for sublist in df["Genre"].dropna().str.split(", ") for genre in sublist) )

genres = list_genres(movies_df)

def recommend_movies(genre = None, mood = None, rating = None, top_n = 5):
    filtered_df = movies_df

    if genres:
        filtered_df = filtered_df[filtered_df["Genre"].str.contains(genre, case=False, na = False)]
    
    if rating:
        filtered_df = filtered_df[filtered_df["IMDB_Rating"]>=rating]
    
    filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)

    recommendations = []

    for idx, row in filtered_df.iterrows():
        overview = row["Overview"]
        if pd.isna(overview):
            continue

        polarity = TextBlob(overview).sentiment.polarity
        if (mood and ((TextBlob(mood).sentiment.polarity < 0 and polarity >0) or polarity >=0)) or not mood:
            recommendations.append((row["Series_Title"], polarity))
        
        if len(recommendations) == top_n:
            break

    return recommendations if recommendations else "No suitable recommendations found based on your criteria."

def display_recommendations(recs, name):
    print(Fore.YELLOW + "AI- Here are your movie recommendations:" + Style.RESET_ALL)
    for i, (title, polarity) in enumerate(recs, 1):
        sentiment = "Positive 😊" if polarity > 0 else "Negative 😞" if polarity < 0 else "Neutral 😐"
        print(Fore.CYAN + f"{i}. {title} - (Polarity: {polarity:.2f}, {sentiment})" + Style.RESET_ALL)

def processing_animation():
    for _ in range(3):
        print(Fore.YELLOW + ".", end = "", flush=True)
        time.sleep(0.5)
    print()


def handle_ai(name):
    print(Fore.BLUE + "Lets find out some movies according to your preferences!")
    
    print(Fore.GREEN + "Available Genres: ", end = " ")
    for idx , g in enumerate(genres, 1):
        print(Fore.CYAN + f"{idx}. {g}")
    
    print()

    while True:
        genre_choice = input(Fore.YELLOW + "Enter a genre number or name from the above list: " + Style.RESET_ALL).strip()
        if genre_choice.isdigit() and 1 <= int(genre_choice) <= len(genres):
            genre = genres[int(genre_choice)-1]
            break
        elif genre_choice.title() in genres:
            genre = genre_choice.title()
            break
        print(Fore.RED + "Invalid genre. Please try again." + Style.RESET_ALL)
    
    mood = input(Fore.YELLOW + "Enter how you currently feel... (Describe your mood): " + Style.RESET_ALL).strip()
    print(Fore.BLUE + "Analyzing Mood", end="", flush=True)
    processing_animation()
    polarity = TextBlob(mood).sentiment.polarity
    mood_desc = "positive 😊" if polarity > 0 else "negative 😞" if polarity < 0 else "neutral 😐"
    print(Fore.GREEN + f"Got it! You seem to be in a {mood_desc} mood. (Polarity: {polarity:.2f})" + Style.RESET_ALL)

    while True:
        rating_input = input(Fore.YELLOW + "Minimum IMDB rating (7.6-9.3, press Enter to skip): " + Style.RESET_ALL).strip()
        if rating_input == "":
            rating = None
            break
        try:
            rating = float(rating_input)
            if 7.6 <= rating <= 9.3:
                break
            print(Fore.RED + "Please enter a rating between 7.6 and 9.3." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a numeric rating." + Style.RESET_ALL)

    print(Fore.BLUE + "Finding recommendations", end="", flush=True)
    processing_animation()

    recs = recommend_movies(genre=genre, mood=mood, rating=rating, top_n=5)
    if isinstance(recs, str):
        print(Fore.RED + recs + "\n"+ Style.RESET_ALL)

    else:
        display_recommendations(recs, name)
        print()

    while True:
        action = input(Fore.YELLOW + "\n Would you like more recommendations? (yes/no): " + Style.RESET_ALL).strip().lower()
        if action in ["no", "n"]:
            print(Fore.GREEN + f"Happy Watching! Goodbye {name}!\n" + Style.RESET_ALL)
            break
        elif action in ["yes", "y"]:
            recs = recommend_movies(genre=genre, mood=mood, rating=rating, top_n=5)
            if isinstance(recs, str):
                print(Fore.RED + recs + "\n"+ Style.RESET_ALL)
            else:
                display_recommendations(recs, name)
        else:
            print(Fore.RED + "Invalid input. Please enter 'yes' or 'no'." + Style.RESET_ALL)

def main():
    print(Fore.GREEN + "Welcome to the Movie Recommendation System powered by AI!" + Style.RESET_ALL)
    name = input(Fore.YELLOW + "Please enter your name: " + Style.RESET_ALL).strip()
    print(Fore.GREEN + f"Hello, {name}! Let's get started.\n" + Style.RESET_ALL)
    handle_ai(name)

if __name__ == "__main__":
    main()





