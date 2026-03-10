from groq import generate_response
import time

def ask_ai(prompt:str, temperature:float):
    start = time.time()

    response = generate_response(
        prompt,
        temp = temperature, 
        max_tokens= 300
    )

    end = time.time()
    print("Response time: ", round(end - start, 2), "seconds")
    return response

def print_header(title):
    print("\n" + "-"*70)
    print(title)
    print("-"*70 + "\n")


def run_activity():
    print_header("Zero Shot, One Shot and Few Shot Example")

    category = input("Enter a category (e.g., 'Animals', 'Countries', 'Famous People'): ").strip()
    item = input(f"Enter a specific {category.lower()}: ").strip()

    if not category or not item:
        print("Please provide both a category and an item.")
        return
    
    zero_prompt = f"""
    Question: Is "{item}" a {category.lower()}?
    Answer: yes or no and explain briefly.
    """

    print_header("ZERO SHOT LEARNING")

    zero_response = ask_ai(zero_prompt, temperature = 0.2)
    print(f"Zero Shot Response:\n{zero_response}\n")

    one_prompt = f"""
    Example: 
    Category: fruit
    Item: apple
    Answer: Yes, apple is a fruit.
    
    Now classify:

    Category: {category}
    Item: {item}
    Answer:
"""
    print_header("ONE SHOT LEARNING")
    one_response = ask_ai(one_prompt, temperature = 0.2)
    print(one_response)



    few_prompt = f"""
    Example 1:
    Category: fruit
    Item: banana
    Answer: Yes, banana is a fruit.

    Example 2:
    Category: animal
    item: lion
    Answer: Yes, lion is an animal.

    Example 3:
    Category: country
    Item: France
    Answer: Yes, France is a country.

    Example 4:
    Category: food
    Item: pizza
    Answer: Yes, pizza is a food.

    Now classify:

    Category: {category}
    Item: {item}
    Answer:
    """

    print_header("FEW SHOT LEARNING")

    few_response = ask_ai(few_prompt, temperature = 0.2)
    print(few_response)


    creative_prompt = f"""
    Write a short imaginative sentence using the word. 
    Example: 

    Word: moon
    Sentence: The moon danced across the night sky, casting a silver glow on the world below.
    
    Now create a sentence using the word "{item}":
    """

    print_header("CREATIVE PROMPT")

    creative_response = ask_ai(creative_prompt, temperature = 0.7)
    print(creative_response)

    print_header("Model Comparision")

    print("ZERO SHOT RESPONSE: ")
    print(zero_response)

    print("\nONE SHOT RESPONSE: ")
    print(one_response)

    print("\nFEW SHOT RESPONSE: ")
    print(few_response)

    print("\nCREATIVE RESPONSE: ")
    print(creative_response)

    print_header("REFECTION QUESTIONS")

    print("1. Which response was the most accurate? ")
    print("2. Did examples improve the AI's answer? ")
    print("3. How did temperature affect creativity?")
    print("4. Why do few-shot prompts guide the model better?")

if __name__ == "__main__":
    run_activity()

