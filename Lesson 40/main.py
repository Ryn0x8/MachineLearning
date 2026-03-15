from groq import generate_response

def bias_mitigation_activity():
    print("\n======BIAS MITIGATION ACTIVITY========")
    prompt = input("Enter a prompt to explore bias: ").strip()
    if not prompt:
        print("Please enter a prompt to run the activity..")
        return
    
    initial_response = generate_response(prompt, temp = 0.3, max_tokens = 1024)
    print("\nInitial Response:\n", initial_response)

    modified_prompt = input(
        "Modify the prompt to mitigate potential bias (e.g., make it more inclusive or neutral): "
    ).strip()
    if modified_prompt:
        modified_response = generate_response(modified_prompt, temp = 0.3, max_tokens = 1024)
        print("\nModified Response:\n", modified_response)
    else:
        print("No modifications made to the prompt. Skipping bias mitigation step.")
    

def token_limit_activity():
    print("\n======TOKEN LIMIT ACTIVITY========")
    long_prompt = input("Enter a long prompt(More than 300 words): ").strip()
    if long_prompt:
        long_response = generate_response(long_prompt, temp = 0.3, max_tokens = 1024)
        preview = (long_response[:500] + "...\n[Response truncated due to token limit]") if len(long_response) > 500 else long_response
        print("\nResponse Preview:\n", preview)
    else:
        print("No long prompt entered. . Skipping Long prompt response.")
    
    short_prompt = input("Now , condense the prompt to be more concise: ").strip()
    if short_prompt:
        short_response = generate_response(short_prompt, temp = 0.3, max_tokens = 1024)
        print("\nShort Prompt Response:\n", short_response)
    else:
        print("No short prompt entered. Skipping short prompt response.")

def run_activity():
    print("======AI LEARNING ACTIVITY=======")
    print("Choose an activity to run:")
    print("1. Bias Mitigation Activity")
    print("2. Token Limit Activity")
    choice = input("> ").strip()
    if choice == "1":
        bias_mitigation_activity()
    elif choice == "2":
        token_limit_activity()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    run_activity()
    
