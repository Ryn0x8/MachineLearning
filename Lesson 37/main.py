from groq import generate_response

import time

def temperature_prompt_activity():
    print("=" * 70)
    print("ADVANCED PROMPT ENGINEERING: TEMPERATURE  + INSTRUCTIONS")
    print("=" * 70)

    print("PART 1: TEMPERATURE")
    base = input("Enter a creative prompt: ").strip()
    for t , label in [
        (0.1, "Low Temperature (0.1) - More Deterministic"),
        (0.5, "Medium Temperature (0.5) - Balanced Creativity"),
        (1.0, "High Temperature (1.0) - More Creative")
    ]:
        print(f"\nGenerating response with {label}...")
        response = generate_response(base, temp=t)
        print(f"Response:\n{response}\n")
        time.sleep(1)
    
    print("PART 2: Instructions")
    topic = input("Enter a topic for instructions (e.g., 'How to make a sandwich'): ").strip()
    prompts = [
        f"Summarize the steps for {topic} in a concise manner.",
        f"Provide detailed instructions for {topic} with examples.",
        f"Explain {topic} in a creative and engaging way."
        f"Create a step-by-step guide for {topic} with tips and warnings."
    ]
    for i, p in enumerate(prompts, 1):
        print(f"\nGenerating response for instruction prompt {i+1}...")
        response = generate_response(p, temp=0.7)
        print(f"Response:\n{response}\n")
        time.sleep(1)
    
    print("Part 3: YOUR OWN INSTRUCTION PROMPT")
    custom = input("Enter your own instruction based prompt: ").strip()
    try:
        temp  = float(input("Set temperature(0.1 to 1.0)"))
        if not (0.1 <= temp <=1.0): raise ValueError
    except ValueError:
        print("Invalid temperature input. Defaulting to 0.7")
        temp = 0.7

    print("\nGenerating response for your custom instruction prompt...")
    response = generate_response(custom, temp=temp)
    print(f"Response:\n{response}\n")

    print("Reflection: How did changing the temperature affect the responses? How did the different instruction prompts guide the model's output? What did you learn about crafting effective prompts for specific types of responses?")
    print("1) Temperature controls the randomness of the model's output. Lower temperatures produce more deterministic and focused responses, while higher temperatures allow for more creativity and variation.")
    print("2) Instruction prompts can guide the model to produce specific types of responses. For example, asking for a summary will yield a concise response, while asking for detailed instructions will result in a more comprehensive answer.")
    print("3) Crafting effective prompts is crucial for getting the desired output from the model. By experimenting with different prompt styles and temperatures, you can better understand how to communicate with the model and achieve your goals.")    

def pseudo_stream(text: str, delay = 0.013):
    for ch in text:
        print(ch, end = "" , flush = True)
        time.sleep(delay)
    print()

def bonus_stream():
    choice = input("BONUS: streaming like output? (y/n): ").lower().strip()
    if choice == "y":
        prompt = input("Enter a prompt for streaming response: ").strip()
        print("\nGenerating streaming response...\n")
        response = generate_response(prompt, temp=0.7)
        pseudo_stream(response)
    else:
        print("Skipping bonus streaming activity.")

if __name__ == "__main__":
    temperature_prompt_activity()
    bonus_stream()