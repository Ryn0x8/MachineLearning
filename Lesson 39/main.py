from groq import generate_response

def reinforcement_learning_activity():
    print("\n======REINFORCEMENT LEARNING ACTIVITY========")
    prompt = input(f"Enter a prompt for the AI Model (e.g, 'Describe the lion'): ").strip()
    if not prompt:
        print("Please enter a prompt to run the activity..")
        return

    initial_response = generate_response(prompt, temp = 0.3, max_tokens = 1024)
    print("\nInitial Response:\n", initial_response)

    try:
        rating = int(input("Rate the response from 1 (bad) to 5 (good): ").strip())
        if rating <1 or rating >5:
            print("Invalid Rating. Using 3")
            rating = 3
    except ValueError:
        print("Invalid Rating. Using 3")
        rating = 3

    feedback = input("Provide feedback for improvement: ").strip()
    improved_response = f"{initial_response} (Immprove with feedback: {feedback})"
    improvised_response = generate_response(improved_response, temp = 0.3, max_tokens = 1024)
    print("\nImproved Response:\n", improvised_response)

    print("\nReflection: ")
    print("1. How did the initial response meet your expectations?")
    print("2. How did your feedback influence the improved response?")

def role_based_prompt_activity():
    print("\n======ROLE-BASED PROMPT ACTIVITY========")
    category = input("Enter a category (e.g., 'science', 'history', 'math'): ").strip()
    item = input(f"Enter a topic in the {category} category: ").strip()
    if not category or not item:
        print("Please provide both a category and an item.")
        return
    
    teacher_prompt = f"You are a teacher explaining {item} in the context of {category}. Provide a clear and concise explanation suitable for a beginner."
    expert_prompt = f"You are an expert in {category}. Provide an in-depth analysis of {item} with advanced insights and technical details."

    teacher_response = generate_response(teacher_prompt, temp = 0.3, max_tokens = 1024)
    expert_response = generate_response(expert_prompt, temp = 0.3, max_tokens = 512)

    print(f"\nTeacher's Response on {item} in {category}:\n", teacher_response)
    print(f"\nExpert's Response on {item} in {category}:\n", expert_response)

    print("\nReflection: ")
    print("1. How did the teacher's response differ from the expert's response?")
    print("2. Which response was more helpful for your understanding of the topic?")


def run_activity():
    print("Choose an activity to run:")
    print("1. Reinforcement Learning Activity")
    print("2. Role-Based Prompt Activity")
    choice = input("Enter the number of the activity you want to run: ").strip()

    if choice == "1":
        reinforcement_learning_activity()
    elif choice == "2":
        role_based_prompt_activity()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    run_activity()