import requests

jokes = []

repeat = 0

def fetch_jokes():
    global repeat
    url = "https://official-joke-api.appspot.com/random_joke"
    if repeat > 5:
        return {"setup": "No new jokes available.", "punchline": "Please try again later."}
    response = requests.get(url)
    if response.status_code == 200:
        if response.json() not in jokes:
            jokes.append(response.json())
            joke = response.json()
        else:
            repeat +=1
            joke = fetch_jokes()
        
    else:
        if response.json() == {"type":"error","message":"Your ip has exceeded the 100 request limit per 15 minute(s). Try again in in 15 minute(s)."}:
            joke = {"setup": "Limit of 100 request Reached.", "punchline": "Please try again later."}
            
        else:
            repeat +=1
            joke = fetch_jokes()

    
    return joke

def print_jokes():
    global repeat
    print("Welcome to Random  Joke Generator")
    print("Press Enter to get a joke or type 'exit' to quit: ")
    while True:
        inp = input()
        if inp.lower() == 'exit':
            print("Goodbye!")
            break
        joke = fetch_jokes()
        print(f"{joke["setup"]} - {joke["punchline"]}")
        repeat = 0

print_jokes()

    
