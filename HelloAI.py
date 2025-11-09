import json

print("Hello I am an AI chatbot. Please Enter your name: ")
name = input()
print(f"Hello {name}, Good to see you")
mood = input("Can you tell me how's your mood today? (Good/Bad): ").lower()

chat_data = {}

if mood == "good":
    print("Glad to hear that you are in a good mood today")
elif mood == "bad":
    print("Sorry to hear that.. I hope your mood gets better after some time...")
else:
    print("I can understand that some times you cant express your feelings or mood into few words...")


chat_data["mood"] = mood
while True:
    print(f"Hey {name}, Do you want to do any more chat?")
    response = input("You can enter Yes/No").lower()
    chat_data["talkMore"] = response
    if response == "yes":
        topic = input("What do you want to talk about today? ")
        chat_data["topic"] = topic
        print(f"That's interesting! I would love to talk about {topic} with you.")
        description = input(f"So {name}, what do you want to talk about on {topic}?")
        chat_data["description"] = description
        print(f"Hey {name}, your description sounded really interesting. I would love to hear more about the topic.")
        more = input("Can you enter more details about it? ")
        chat_data["more"] = more
        print(f"Thanks for sharing more about {topic}, {name}. It was great talking to you about it!")
        
        with open("chat_data.json", "r") as f:
            data = json.load(f)
    

        with open("chat_data.json", "w") as f:
            if name not in data:
                data[name] = chat_data
            else:
                data[name + "_1"] = chat_data
            json.dump(data, f, indent=4)
        
        break
    else:
        with open("chat_data.json", "r") as f:
            data = json.load(f)
    

        with open("chat_data.json", "w") as f:
            if name not in data:
                data[name] = chat_data
            else:
                data[name + "_1"] = chat_data
            json.dump(data, f, indent=4)
        break

print(f"I am very happy to have a talk with you {name}! I hope to talk with you again someday")

