from hf import generate_response

def prompt_engineering_activity():
    print("Welcome to the Prompt Engineering Activity!")

    vague = input("Enter a vague prompt: ")
    print("\nGenerating response for vague prompt...")
    vague_response = generate_response(vague)
    print(f"Response to vague prompt:\n{vague_response}\n")

    specific = input("Now, enter a more specific prompt: ")
    print("\nGenerating response for specific prompt...")
    specific_response = generate_response(specific)
    print(f"Response to specific prompt:\n{specific_response}\n")

    context = input("Finally, enter a prompt with additional context: ")
    print("\nGenerating response for prompt with context...")
    context_response = generate_response(context)
    print(f"Response to prompt with context:\n{context_response}\n")

    print("Notice how the responses differ based on the specificity and context of the prompts. This is the essence of prompt engineering!")
    print("Reflection: Prompt engineering is a critical skill in working with AI models. By carefully crafting prompts, we can guide the model to produce more accurate, relevant, and useful outputs.")
    print("How did the responses differ based on the prompts you provided? What did you learn about the importance of prompt engineering?")

if __name__ == "__main__":
    prompt_engineering_activity()