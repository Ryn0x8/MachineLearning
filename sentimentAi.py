import colorama
from colorama import Fore, Style
from textblob import TextBlob

colorama.init(autoreset=True)

print(f"{Fore.CYAN} Hello! Welcome to Sentiment Spy! {Style.RESET_ALL}")
while True:
    user_name = input(f"{Fore.YELLOW} Please enter your name: {Style.RESET_ALL}").strip()
    if user_name and user_name.isalpha(): 
        break
    else:
        print(f"{Fore.RED}Please enter a valid name with only alphabetic characters.")

conversation_history = []

positive_count, negative_count, neutral_count = 0, 0, 0

def show_processing_animation():
    print(f"{Fore.CYAN} Analyzing sentiment", end="")
    for _ in range(3):
        print(f"{Fore.CYAN}.", end="", flush=True)
        import time
        time.sleep(0.5)
    print("\n")

def save_sentiment_data():
    with open(f"SentimentData/{user_name}_sentiment_data.txt", "w") as f:
        f.write(f"Sentiment Analysis Data for Agent: {user_name}\n")
        f.write("Positive Count: {}\n".format(positive_count))
        f.write("Negative Count: {}\n".format(negative_count))
        f.write("Neutral Count: {}\n".format(neutral_count))
        f.write("\nConversation History:\n")
        for text, sentiment_type, polarity in conversation_history:
            f.write(f"{text} | Sentiment: {sentiment_type} (Polarity: {polarity})\n")

def analyze_sentiment(text):
    global positive_count, negative_count, neutral_count
    message = text
    polarity = TextBlob(message).sentiment.polarity
    if polarity > 0.25:
        sentiment_type = "Positive"
        positive_count += 1
        color = Fore.GREEN
        emoji = "😊"
    elif polarity <-0.25:
        negative_count += 1
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😭"
    else:
        neutral_count += 1
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😑"

    print(f"{color}{emoji} {sentiment_type} sentiment detected"
            f"(Polarity: {polarity:.2f})"
          )
    conversation_history.append((message, sentiment_type, polarity))

def help_show():
    print(f"{Fore.CYAN} You can enter any message to analyze its sentiment.")
    print(f"Type 'history' to see conversation history.")
    print(f"Type 'reset' to clear conversation history.")
    print(f"Type 'exit' to quit the program.")
    print(f"Type 'summary' to see sentiment summary.")

print(f"{Fore.CYAN} Hello Agent {user_name}, I am Sentiment Spy who will analyze your sentiment through TextBlob..{Style.RESET_ALL}")
help_show()


while True:
    message = input(f"{Fore.GREEN} >>").strip()
    if not message:
        print(f"{Fore.RED} Please enter a valid message. {Style.RESET_ALL}")
        continue
    if message.lower() == 'exit':
        print(f"{Fore.CYAN} Goodvbye Agent {user_name}! Stay Positive and hope to talk with you again")
        save_sentiment_data()
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

    elif message.lower() == "summary":
        total_messages = len(conversation_history)
        positive_count = sum(1 for _, sentiment_type, _ in conversation_history if sentiment_type == "Positive")
        negative_count = sum(1 for _, sentiment_type, _ in conversation_history if sentiment_type == "Negative")
        neutral_count = sum(1 for _, sentiment_type, _ in conversation_history if sentiment_type == "Neutral")

        print(f"{Fore.CYAN} Sentiment Summary:")
        print(f"Total Messages Analyzed: {total_messages}")
        print(f"{Fore.GREEN} Positive: {positive_count} ")
        print(f"{Fore.RED} Negative: {negative_count} ")
        print(f"{Fore.YELLOW} Neutral: {neutral_count} ")
        continue
    
    elif message.lower() == 'help':
        help_show()
        continue
    
    show_processing_animation()
    analyze_sentiment(message)

                

