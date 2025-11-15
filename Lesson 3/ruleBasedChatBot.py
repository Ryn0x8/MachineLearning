import re, random, datetime
from colorama import Fore
import colorama

colorama.init(autoreset=True)

memory = {
    "last_topic": None
}

destinations = {
    "cities": ["New York", "Paris", "Tokyo", "Sydney", "Cairo"],
    "beaches": ["Maldives", "Bora Bora", "Bahamas", "Phuket", "Maui"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas", "Andes", "Appalachians"]
}

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't skeletons fight each other? They don't have the guts!"
]

weather_conditions = [
    "Sunny with clear skies.",
    "Cloudy with a chance of rain.",
    "Heavy rainfall expected.",
    "Thunderstorms approaching!",
    "Cool and breezy today."
]

news_headlines = [
    "Global markets show signs of recovery.",
    "New technological breakthrough shocks the world!",
    "Scientists discover a new species in the Amazon rainforest.",
    "Sports update: Underdog team wins championship!",
    "Space agency announces new lunar mission."
]

city_timezones = {
    "new york": -5,
    "paris": 1,
    "tokyo": 9,
    "sydney": 10,
    "kathmandu": 5.75,
    "london": 0,
    "dubai": 4
}

def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def match_keywords(user_input, keywords):
    return any(re.search(rf"\b{kw}\b", user_input) for kw in keywords)

def recommend(category=None):
    memory["last_topic"] = "recommendation"
    if category is None:
        print(f"{Fore.CYAN}CHATBOT: Looking for travel ideas? Choose cities, beaches, or mountains!")
        category = normalize_input(input(Fore.YELLOW + "User: "))
    if category in destinations:
        suggestion = random.choice(destinations[category])
        print(f"{Fore.CYAN}CHATBOT: How about visiting {suggestion}?")
        feedback = normalize_input(input(Fore.YELLOW + "Did you like the suggestion? (yes/no): "))
        if feedback == "yes":
            print(f"{Fore.GREEN}CHATBOT: Awesome! Have a great trip to {suggestion}!")
        else:
            print(f"{Fore.RED}CHATBOT: No worries! Let me suggest another one.")
            recommend(category)
    else:
        print(f"{Fore.RED}CHATBOT: Invalid category. Restarting recommendation...")
        recommend()
    show_help(True)

def packing_tips():
    memory["last_topic"] = "packing"
    tips = [
        "Make a packing list to stay organized.",
        "Roll your clothes to save space.",
        "Bring versatile clothing.",
        "Don't forget chargers & adapters!",
        "Carry a small first-aid kit."
    ]
    dest = normalize_input(input(Fore.YELLOW + "Where are you traveling to?\nUser: "))
    time = normalize_input(input(Fore.YELLOW + f"How long will you stay in {dest.title()}?\nUser: "))
    print(f"{Fore.CYAN}Here are packing tips for {dest.title()} ({time} stay):")
    for i, t in enumerate(tips, 1):
        print(Fore.GREEN + f"{i}. {t}")
    show_help(True)

def tell_joke():
    memory["last_topic"] = "joke"
    print(Fore.MAGENTA + "CHATBOT: " + random.choice(jokes))
    show_help(True)

def weather_report():
    memory["last_topic"] = "weather"
    city = normalize_input(input(Fore.YELLOW + "Enter a city for weather info:\nUser: "))
    report = random.choice(weather_conditions)
    print(Fore.CYAN + f"CHATBOT: The weather in {city.title()} right now: {report}")
    show_help(True)

def news_update():
    memory["last_topic"] = "news"
    print(Fore.CYAN + "CHATBOT: Here are today's top headlines:")
    for i in random.sample(news_headlines, 3):
        print(Fore.GREEN + "• " + i)
    show_help(True)

def city_time():
    memory["last_topic"] = "time"
    city = normalize_input(input(Fore.YELLOW + "Enter a city name:\nUser: "))
    if city not in city_timezones:
        print(Fore.RED + "Sorry, I don't know the time for that city.")
    else:
        offset = city_timezones[city]
        utc_now = datetime.datetime.utcnow()
        local_time = utc_now + datetime.timedelta(hours=offset)
        print(Fore.CYAN + f"Current time in {city.title()}: {local_time.strftime('%H:%M:%S')}")
    show_help(True)

def show_help(repeat=False):
    print(Fore.CYAN + ("Anything else I can help with?" if repeat else "Here’s what I can do:"))
    print(Fore.YELLOW + """
1. Travel recommendations → 'recommend'
2. Packing tips → 'packing'
3. Tell a joke → 'joke'
4. Weather info → 'weather'
5. News updates → 'news'
6. Local time in cities → 'time'
7. Exit → 'exit'
""")

def main():
    name = normalize_input(input(Fore.YELLOW + "CHATBOT: Please enter your name:\nUser: "))
    if not name:
        name = "Traveler"
    print(Fore.GREEN + f"Hello {name.title()}! I’m your upgraded Rule-Based Chatbot!")
    show_help()
    while True:
        user_input = normalize_input(input(Fore.YELLOW + f"{name.title()}: "))
        if match_keywords(user_input, ["recommend", "suggest"]):
            recommend()
        elif match_keywords(user_input, ["pack", "packing"]):
            packing_tips()
        elif match_keywords(user_input, ["joke", "funny"]):
            tell_joke()
        elif match_keywords(user_input, ["weather", "temperature"]):
            weather_report()
        elif match_keywords(user_input, ["news", "headline"]):
            news_update()
        elif match_keywords(user_input, ["time", "clock"]):
            city_time()
        elif match_keywords(user_input, ["exit", "quit"]):
            print(Fore.CYAN + f"Goodbye {name.title()}! Have a wonderful day.")
            break
        else:
            print(Fore.RED + "Sorry, I didn’t understand that.")
            show_help()

if __name__ == "__main__":
    main()
