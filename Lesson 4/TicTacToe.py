from colorama import Fore, init, Style
import random

init(autoreset=True)

def display_board(board):
    print()

    def colored(cell):
        if cell == "X":
            return Fore.RED + cell + Style.RESET_ALL
        elif cell == "O":
            return Fore.BLUE + cell + Style.RESET_ALL
        else:
            return Fore.YELLOW + cell + Style.RESET_ALL
        
    print(f" {colored(board[0])} | {colored(board[1])} | {colored(board[2])} ")
    print(Fore.CYAN + "-----------" + Style.RESET_ALL)
    print(f" {colored(board[3])} | {colored(board[4])} | {colored(board[5])} ")
    print(Fore.CYAN + "-----------" + Style.RESET_ALL)
    print(f" {colored(board[6])} | {colored(board[7])} | {colored(board[8])} ")
    print()

def player_choice():
    symbol = ""
    while symbol not in ["X", "O"]:
        symbol = input(Fore.YELLOW + "Choose your symbol (X/O): ").upper()
        if symbol == "X":
            print(Fore.GREEN + "You chose X! You will go first." + Style.RESET_ALL)
            return "X", "O"
        elif symbol == "O":
            print(Fore.GREEN + "You chose O! The computer will go first." + Style.RESET_ALL)
            return "O", "X"
    
def player_move(board, symbol):
    move = -1
    while move not in range(1, 10) or board[move-1] in ["X", "O"]:
        try:
            move = int(input(Fore.YELLOW + "Enter your move (1-9): "))
            if move not in range(1, 10):
                print(Fore.RED + "Invalid input. Please enter a number between 1 and 9." + Style.RESET_ALL)
            elif board[move-1] in ["X", "O"]:
                print(Fore.RED + "That cell is already taken. Choose another one." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a number between 1 and 9." + Style.RESET_ALL)
    board[move-1] = symbol

def ai_move(board, ai_symbol, player_symbol):
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = ai_symbol
            if check_winner(board_copy, ai_symbol):
                board[i] = ai_symbol
                return
    
    for i in range(9):
        if board[i].isdigit():
            board_copy = board.copy()
            board_copy[i] = player_symbol
            if check_winner(board_copy, player_symbol):
                board[i] = ai_symbol
                return
    
    available_moves = [i for i in range(9) if board[i].isdigit()]
    ai_move = random.choice(available_moves)
    board[ai_move] = ai_symbol

def check_winner(board, symbol):
    winning_position = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1, 4, 7), (2,5,8),
        (0, 4, 8), (2, 4, 6)
    ]

    for pos in winning_position:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == symbol:
            return True
    return False

def spot_full(board):
    return all(not cell.isdigit() for cell in board)

def tic_tac_toe():
    print(Fore.GREEN + "Welcome to Tic-Tac-Toe!" + Style.RESET_ALL)
    name = input(Fore.YELLOW + "Enter your name: " + Style.RESET_ALL)
    while True:
        game_on = True
        board = [str(i) for i in range(1, 10)]
        player_symbol, ai_symbol = player_choice()
        Trun = player_symbol == "X"
        while game_on:
            display_board(board)
            if Trun:
                player_move(board, player_symbol)
                if check_winner(board, player_symbol):
                    display_board(board)
                    print(Fore.GREEN + f"Congratulations {name}, you win!" + Style.RESET_ALL)
                    game_on = False
                else:
                    if spot_full(board):
                        display_board(board)
                        print(Fore.CYAN + "It's a tie!" + Style.RESET_ALL)
                        game_on = False
                    else:
                        Trun = False
                
            else:
                ai_move(board, ai_symbol, player_symbol)
                if check_winner(board, ai_symbol):
                    display_board(board)
                    print(Fore.RED + "The computer wins! Better luck next time." + Style.RESET_ALL)
                    game_on = False
                else:
                    if spot_full(board):
                        display_board(board)
                        print(Fore.CYAN + "It's a tie!" + Style.RESET_ALL)
                        game_on = False
                    else:
                        Trun = True

        replay = input(Fore.YELLOW + "Do you want to play again? (yes/no): ").lower()
        if replay != "yes":
            print(Fore.GREEN + "Thanks for playing Tic-Tac-Toe! Goodbye!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    tic_tac_toe()


