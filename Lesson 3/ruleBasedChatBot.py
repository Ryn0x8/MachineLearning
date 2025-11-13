import re, random
from colorama import Fore
import colorama

colorama.init(autoreset=True)

print(f"{Fore.GREEN} Hello User! Welcome to the Rule-Based Chat Bot!")

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

def normalize_input(inputt):
    return re.sub(r"\s+", " ", inputt.strip().lower())

def recommend(category = None):
    if category is None:
        print(f"CHATBOT: {Fore.CYAN} Hey User! looking for some travel recommendations? Want me to help?")
        category = input(f"{Fore.YELLOW} If yes, Please enter the category (cities, beaches, mountains) or enter exit to close\nUser:").strip().lower()
        category = normalize_input(category)
        if category == "exit":
            print(f"CHATBOT: {Fore.CYAN} Goodbye User! Hope to assist you again!")
            return
    
    if category in destinations:
        suggestion = random.choice(destinations[category])
        print(f"CHATBOT: {Fore.CYAN} Hey How about you try visiting {suggestion}?")
        print(f"CHATBOT: {Fore.CYAN} Did you like it User? (Yes/No)?")
        feedback = input(f"{Fore.YELLOW} User:").strip().lower()
        feedback = normalize_input(feedback)
        if feedback == 'yes':
            print(f"CHATBOT: {Fore.CYAN} Awesome! Hope you have a great trip to {suggestion}!")
        else:
            print(f"CHATBOT: {Fore.RED} No Worries Let Me suggest you something else for {category}")
            recommend(category)
    else:
        print(f"CHATBOT: {Fore.RED} Sorry User, I don't have recommendations for that category. Please choose from cities, beaches, or mountains. Lets Start it Over Again")
        recommend()
    show_help(True)

def packing_tips():
    tips = [
        "Make a packing list to ensure you don't forget essentials.",
        "Roll your clothes to save space and reduce wrinkles.",
        "Pack versatile clothing that can be mixed and matched.",
        "Don't forget chargers and adapters for your electronics.",
        "Bring a small first aid kit for emergencies."
    ]
    print(f"CHATBOT: {Fore.CYAN} Hey User! Where are you traveling to?")
    destination = input(f"{Fore.YELLOW} User:").strip()
    destination = normalize_input(destination)
    time = input(f"{Fore.CYAN} CHATBOT: Great! How long will you be staying in {destination.title()}?\n{Fore.YELLOW} User:").strip()
    time = normalize_input(time)
    print(f"{Fore.CYAN} CHATBOT: Here are some packing tips for your trip to {destination.title()} for {time}:")
    for idx, tip in enumerate(tips, start=1):
        print(f"{idx}. {tip}")
    
    show_help(repeat=True)

def tell_joke():
    print(f"CHATBOT: {Fore.CYAN} Here's a joke for you: {random.choice(jokes)}")
    show_help(True)

def show_help(repeat = False):
    if not repeat:
        print(f"CHATBOT: Heres a list of everything I can do for you:")
    else:
        print(f"CHATBOT: {Fore.CYAN} Is there anything else I can help you with? Here's what I can do for you again:")
    print(f"{Fore.YELLOW} 1. Recommend travel destinations (type 'recommend')")
    print(f"{Fore.YELLOW} 2. Provide packing tips (type 'packing')")
    print(f"{Fore.YELLOW} 3. Tell a joke (type 'joke')")
    print(f"{Fore.YELLOW} 4. Exit the chat (type 'exit')")

def main():
    name = input(f"{Fore.YELLOW}CHATBOT: Please enter your name:\nUser:").strip()
    name = normalize_input(name)
    if not name:
        name = "Traveler"
    
    print(f"{Fore.CYAN} CHATBOT: Hello {name.title()}! I'm your Rule-Based Chat Bot here to assist you with travel recommendations, packing tips, and more!")
    show_help()
    while True:
        user_input = input(f"{Fore.YELLOW}{name.title()}:")
        user_input = normalize_input(user_input)
        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "packing" in user_input or "pack" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "exit" in user_input or "quit" in user_input:
            print(f"{Fore.CYAN} CHATBOT: Goodbye {name.title()}! Safe travels and hope to chat with you again!")
            break
        else:
            print(f"{Fore.RED}CHATBOT: Sorry {name.title()}, I didnt understand your message.")
            show_help()

if __name__ == "__main__":
    main()



