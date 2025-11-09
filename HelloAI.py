print("Hello I am an AI chatbot. Please Enter your name: ")
name = input()
print(f"Hello {name}, Good to see you")
mood = input("Can you tell me how's your mood today? (Good/Bad): ").lower()

if mood == "good":
    print("Glad to hear that you are in a good mood today")
elif mood == "bad":
    print("Sorry to hear that.. I hope your mood gets better after some time...")
else:
    print("I can understand that some times you cant express your feelings or mood into few words...")

print(f"I am very happy to have a talk with you {name}! I hope to talk with you again someday")

