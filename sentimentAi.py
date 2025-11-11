import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init(autoreset=True)

print(f"{Fore.CYAN} Hello! Welcome to Sentiment Spy! {Style.RESET_ALL}")

user_name = input(f"{Fore.YELLOW} Please enter your name: {Style.RESET_ALL}").strip()
if not user_name:
    user_name = "Mystery Agent"

conversation_history = []

print(f"{Fore.CYAN} Hello Agent {user_name}, I am Sentiment Spy who will analyze your sentiment through TextBlob..{Style.RESET_ALL}")
print(f"{Fore.YELLOW} Please enter your messages below. Type 'history' to see conversation history , 'reset' to reset the conversation history and 'exit' to quit the program.{Style.RESET_ALL}")

while True:
    message = input(f"{Fore.GREEN} >>").strip()
    if not message:
        print(f"{Fore.RED} Please enter a valid message. {Style.RESET_ALL}")
        continue
    if message.lower() == 'exit':
        print(f"{Fore.CYAN} Goodvbye Agent {user_name}! Stay Positive and hope to talk with you again")
        break
    elif message.lower() == 'reset':
        conversation_history.clear()
        print(f"{Fore.CYAN} Agent, Conversation history has been cleared. You can start fresh again!!")
        continue
    elif message.lower() == 'history':
        if not conversation_history:
            print(f"{Fore.CYAN} Agent, You dont have any conversation history yet!")
        else:
            print(f"{Fore.CYAN} Conversation History: ")
            for idx, (text, sentiment_type, polarity) in enumerate(conversation_history, start=1):
                if sentiment_type.lower() == "positive":
                    color = Fore.GREEN
                    emoji = "😊"
                elif sentiment_type.lower() == "negative":
                    color = Fore.RED
                    emoji = "😭"
                else:
                    color = Fore.YELLOW
                    emoji = "😐"

                print(f"{idx}. {color}{emoji} {text} | Sentiment: {sentiment_type} (Polarity: {polarity})")
        continue

    polarity = TextBlob(message).sentiment.polarity
    if polarity > 0.25:
        sentiment_type = "Positive"
        color = Fore.GREEN
        emoji = "😊"
    elif polarity <-0.25:
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😭"
    else:
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😑"

    print(f"{color}{emoji} {sentiment_type} sentiment detected"
            f"(Polarity: {polarity:.2f})"
          )
    conversation_history.append((message, sentiment_type, polarity))

                

