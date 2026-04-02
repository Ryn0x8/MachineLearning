from hf import generate_response

def get_essay_details():
    print("\n===== AI Writing Assistant == \n")
    topic = input("What is the topic of your essay? ").strip()
    essay_type = input("What type of essay are you writing? (e.g., argumentative, descriptive, narrative): ").strip()
    lengths = ["300 words", "900 words", "1200 words", "2000 words"]
    print("Select Essay Word count: ")
    for i, l in enumerate(lengths, 1): print(f"{i}. {l}")
    try:
        idx = int(input("> ").strip()) - 1
        length = lengths[idx] if 0<= idx < len(lengths) else "300 words"
    except ValueError:
        length  = "300 words"

    target_audience = input("Who is the target audience for your essay? ").strip()
    return topic, essay_type, length, target_audience

def generate_essay_content(details):
    topic, essay_type, length, target_audience = details["topic"], details["essay_type"], details["length"], details["target_audience"]
    try:
        temp = float(input("Enter temperature (0.1 structured, 0.7 creative): ").strip())
        if not (0.0 <= temp <=1.0): raise ValueError
    except ValueError:
        print("Invalid temperature. Using default value of 0.3.")
        temp = 0.3

    intro_p = f"Write an introduction for a {essay_type} essay on the topic '{topic}' targeting {target_audience} with total length of {length}."
    intro = generate_response(intro_p, temp=temp, max_tokens=1024)
    print("\nGenerated Introduction:\n", intro)

    print("\n WOuld you like the body written as full draft or step by step?")
    print("1. Full Draft")
    print("2. Step by Step")
    choice = input("> ").strip()

    if choice == "1":
        body_p = f"Write a full body for the {essay_type} essay on '{topic}' targeting {target_audience}. Include supporting arguments, evidence, and examples."
        body = generate_response(body_p, temp=temp, max_tokens=2048)
        print("\nGenerated Body:\n", body)

    else:
        step_p = f"Write a step by step arguments for an essay on '{topic}' targeting {target_audience}. Provide evidence and reasoning"
        body_steps = generate_response(step_p, temp=temp, max_tokens=2048)
        print("\nGenerated Body Step by step:\n", body_steps)

    conclusion_p = f"Write a conclusion for the {essay_type} essay on '{topic}' targeting {target_audience}. Summarize key points and provide a closing thought."
    conclusion = generate_response(conclusion_p, temp=temp, max_tokens=1024)
    print("\nGenerated Conclusion:\n", conclusion)

def feedback_and_refinement():
    try: 
        rating = int(input("\nRate the generated essay content on a scale of 1 to 5 (1 = poor, 5 = excellent): ").strip())
        if rating < 1 or rating > 5: raise ValueError
    except ValueError:
        print("Invalid rating. Using 3.")
        rating = 3

    if rating != 5:
        feedback = input("Please provide specific feedback on what could be improved: ").strip()
        print("Thank you for your feedback! The AI will use this to improve future responses.")
    else:
        print("Great! We're glad you found the content helpful. Your feedback helps us improve our AI models.")

def run_activity():
    print("Welcome to the AI Writing Assistant")
    (topic, essay_type, length, target_audience) = get_essay_details()
    details = {
        "topic": topic,
        "essay_type": essay_type,
        "length": length,
        "target_audience": target_audience
    }
    if not topic or not essay_type:
        print("Please provide atleast a topic and a essay type to continue.")
        return
    generate_essay_content(details)
    feedback_and_refinement()

if  __name__ == "__main__":
    run_activity()

