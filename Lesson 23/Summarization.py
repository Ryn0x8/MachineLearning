import requests
from config import HF_API
from colorama import Fore, Style, init

init(autoreset=True)

default_model = "google/pegasus-xsum"

def build_api_url(model_name):
    return f"https://router.huggingface.co/hf-inference/models/{model_name}"

def query(payload, model_name = default_model):
    API = build_api_url(model_name)
    headers = {
        "Authorization": f"Bearer {HF_API}"
    }
    response = requests.post(API, headers=headers, json = payload)
    return response.json()

def summarize_text(text, max_length, min_length, model_name = default_model):
    payload = {
        "inputs": text,
        "parameters":{
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False
        }
    }
    response = query(payload, model_name)

    if isinstance(response, dict) and "error" in response:
        print(Fore.RED + "Error:", response["error"])
        return None

    try:
        return response[0]["summary_text"]

    except (KeyError, IndexError, TypeError) as e:
        print(Fore.RED + "Error processing response:", e)
        print(Fore.RED + "Response content:", response)
        return None
    
if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "Hellow Friend! Whats your name?")
    name = input().strip()
    if not name:
        name = "User"
    
    print(Fore.CYAN + f"Welcome, {name}! Let's summarize some text.")
    print(Fore.YELLOW + "Please enter the text you want to summarize:")
    text = input("> ").strip()
    if not text:
        print(Fore.RED + "No text provided. Exiting.")
        exit(1)
    
    model_choice = input(Fore.YELLOW + "Enter model name (or press Enter to use default - google/pegasus-xsum): ").strip()
    if not model_choice:
        model_choice = default_model
    
    print(Fore.YELLOW + "Please choose your summarization style: ")
    print(Fore.GREEN + "1. Standard Summary (Quick and Concise)")
    print(Fore.GREEN + "2. Detailed Summary (More Comprehensive)")

    style_choice = input("> ").strip()
    if style_choice == "2":
        max_len = 300
        min_len = 200
        print("Detailing summarization process...")
    else:
        max_len = 150
        min_len = 50
        print("Standard summarization process...")
    
    summary = summarize_text(text, max_len, min_len, model_choice)
    if summary:
        print(Fore.CYAN + Style.BRIGHT + "\nHere is your summary:\n")
        print(Fore.WHITE + Style.BRIGHT+ summary)
    else:
        print(Fore.RED + "Failed to generate summary.")

