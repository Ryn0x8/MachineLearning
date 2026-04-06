from groq import generate_response
import re
import streamlit as st
import time
import random

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) <10:
        return True
    
    t = text.strip()

    if t.endswith(("**", "*", "-", ":", "(", "[", "{", "```", "```")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):
        return True
    if not re.search(r"[.!?](['\"])?\s*$", t):
        return True
    return False

def complete_answer(q: str, max_r: int = 2) -> str:
    base_prompt = f"""
        Answer clearly in numered points
        Do not cut sentences. Finish each point fully.
        fAnswer this Question: {q}
    """

    ans = generate_response(base_prompt, temp=0.3, max_tokens=1024)

    rounds = 0
    while rounds < max_r and looks_incomplete(ans):
        followup_prompt = {
            "Continue the answer to the following question. Do not repeat what has already been said. Answer in numbered points and do not cut sentences.\n\n"
            f"Question: {q}\n\nCurrent Answer: {ans}\n\nContinue the answer:"
        }
        more = generate_response(followup_prompt, temp=0.3, max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = ans.strip() + "\n" + more.strip()
        rounds += 1
    return ans.strip()

def main():
    st.title("AI Teaching Assistant")
    st.write("Welcome! You can ask me any question related to the course material, and I'll do my best to provide a clear and complete answer. If my initial response is incomplete, I'll automatically continue until I provide a full answer.")

    user_input = st.text_input("Enter your question here:")
    if user_input:
        with st.spinner("Generating answer..."):
            answer = complete_answer(user_input)
        st.subheader("Answer:")
        placeholder = st.empty()
        typed_ans = ""
        for char in answer:
            typed_ans += char
            placeholder.markdown(typed_ans + ".")
            time.sleep(0.001)
            placeholder.markdown(typed_ans + "..")
            time.sleep(0.001)
            placeholder.markdown(typed_ans + "...")
            time.sleep(0.001)

            if char in ".!?":
                time.sleep(random.uniform(0.2, 0.5))  # pause at sentence end
            elif char == ",":
                time.sleep(random.uniform(0.1, 0.3))  # slight pause
            else:
                time.sleep(random.uniform(0.01, 0.05))  # fast typing
        placeholder.markdown(typed_ans)  
    else:
        st.info("Please enter a question to get started.")

if __name__ == "__main__":
    main()
