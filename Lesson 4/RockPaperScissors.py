import random
from colorama import Fore, Style, init

init(autoreset=True)

moves = ["rock", "paper", "scissors"]
emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
player_history = []

def advanced_ai_choice(history):
    if not history:
        return random.choice(moves)
    freq = {m: history.count(m) for m in moves}
    predicted = max(freq, key=freq.get)
    if predicted == "rock":
        return "paper"
    elif predicted == "paper":
        return "scissors"
    else:
        return "rock"

def ai_move(use_advanced_ai=True):
    if use_advanced_ai:
        return advanced_ai_choice(player_history)
    return random.choice(moves)

def determine_winner(player, ai):
    if player == ai:
        return "tie"
    if (player == "rock" and ai == "scissors") or (player == "scissors" and ai == "paper") or (player == "paper" and ai == "rock"):
        return "player"
    return "ai"

def play_game():
    player_score = 0
    ai_score = 0
    print(Fore.CYAN + "🎮 Welcome to Rock–Paper–Scissors with AI 🤖")
    print("Type 'exit' to quit.\n")

    while True:
        player = input(Fore.YELLOW + "Choose Rock, Paper, or Scissors: ").lower()
        if player == "exit":
            break
        if player not in moves:
            print(Fore.RED + "Invalid move ⚠️\n")
            continue

        player_history.append(player)
        ai = ai_move(True)
        winner = determine_winner(player, ai)

        print(Fore.MAGENTA + f"AI chose: {ai} {emojis[ai]}")

        if winner == "player":
            print(Fore.GREEN + "🎉 You win this round!\n")
            player_score += 1
        elif winner == "ai":
            print(Fore.RED + "🤖 AI wins this round!\n")
            ai_score += 1
        else:
            print(Fore.BLUE + "😐 It's a tie!\n")

        print(Fore.CYAN + f"Score → You: {player_score} | AI: {ai_score}\n")

    print(Fore.CYAN + "\n🏁 Final Score:")
    print(Fore.GREEN + f"You: {player_score}" + Fore.RED + f" | AI: {ai_score}")
    print(Fore.MAGENTA + "Thanks for playing! 👋")

play_game()
