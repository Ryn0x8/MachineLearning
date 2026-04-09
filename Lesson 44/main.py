from hf import generate_response

import io
import streamlit as st
import re

CSS = """
<style>

/* Page background */
body {
    background-color: #0f172a;
}

/* History scroll */
.history-wrap {
    max-height: 450px;
    overflow-y: auto;
    padding-right: 8px;
}

/* Card style */
.qa-card {
    border-radius: 14px;
    background: linear-gradient(145deg, #1e293b, #0f172a);
    padding: 16px 18px;
    margin: 12px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    transition: transform 0.2s ease;
}

.qa-card:hover {
    transform: translateY(-2px);
}

/* Question */
.q {
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 6px;
    font-size: 15px;
}

/* Answer */
.a {
    white-space: pre-wrap;
    color: #e2e8f0;
    line-height: 1.6;
    font-size: 14px;
}

/* Scrollbar (nice touch) */
.history-wrap::-webkit-scrollbar {
    width: 6px;
}

.history-wrap::-webkit-scrollbar-thumb {
    background: #475569;
    border-radius: 10px;
}

</style>
"""

SYSTEM_PROMPT = """You are a Math Mastermind. For every math problem: 
1) Show step-by-step solution   2) Explain the reasoning   3) Give alternative method if possible
4) verify answer if possible    5) Use proper notation    6) Break complex problems into parts
Format: Problem -> Steps -> **Final Answer** -> Concepts Used. Be Precise and educational  
"""

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) <10:
        return True
    
    t = text.strip()

    if t.endswith(("**", "*", "-", ":", "(", "[", "{")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):
        return True
    return False


def export_bytes(history):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i,h in enumerate(history, 1)])
    return io.BytesIO(text.encode("utf-8"))

def complete_answer(q: str, level:str, max_tokens:int = 2048,max_r: int = 2, temp: float = 0.1) -> str:
    base_prompt = f"""
        {SYSTEM_PROMPT}\n\nMath Problem ({level}): {q}
    """

    ans = generate_response(base_prompt, temp=temp, max_tokens = max_tokens)

    rounds = 0
    while rounds < max_r and looks_incomplete(ans):
        followup_prompt = f"""
            Continue the answer to the following question. Do not repeat what has already been solved. Complete the remaining solutions.\n\n
            Question: {q}\n\nCurrent Answer: {ans}\n\nContinue the answer:
        """
        more = generate_response(followup_prompt, temp=temp, max_tokens=max_tokens)
        if not more or more.strip() in ans:
            break
        ans = ans.strip() + "\n" + more.strip()
        rounds += 1
    return ans.strip()

def setup_ui():
    st.set_page_config(page_title="Math MasterMind", page_icon=":robot_face:", layout="centered")
    st.title("Math MasterMind")
    st.write("Solve any math problem with detailed step-by-step explanations")
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("k", 0)

    with st.expander("Examples: "):
        st.markdown(
        "- Algebra: Solve for x 2x + 3 = 7\n"
        "- Calculus: Differentiate f(x) = 3x^2 + 5"
        "- Geometry: Find the area of a circle with radius r\n"
        "- Probability: What is the probability of rolling a sum of 7 with two dice?"
        )

    col1, col2 = st.columns([1,2])

    with col1:
        if st.button("🧹 Clear"):
            st.session_state.history = []
            st.rerun()

    with col2:
        if st.session_state.history:
            st.download_button(
                label="⬇ Export",
                data=export_bytes(st.session_state.history),
                file_name="qa_history.txt",
                mime="text/plain"
            )

    with st.form("math_form", clear_on_submit = True):
        q = st.text_area("💬 Enter your math problem here...", height=120, placeholder="e.g., Solve for x: 2x + 3 = 7", key = f"q_{st.session_state.k}")
        a,b = st.columns([3,1])
        solve = a.form_submit_button("Solve", use_container_width = True)
        level = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index = 1)
        if solve:
            if not q.strip(): st.warning("Enter a problem first..")
            else:
                with st.spinner("Solving problem..."):
                    a = complete_answer(q, level, max_r=4, temp=0.1)
                st.session_state.history.insert(0, {"question": q, "answer": a})
                st.session_state.k += 1
                st.rerun()
        
    
    if not st.session_state.history: return
    st.markdown("### Conversation History")
    st.markdown(CSS, unsafe_allow_html=True)

    cards = []
    for i,h in enumerate(st.session_state.history, 1):
        cards.append(f"<div class='qa-card'><div class='q'>Q{i}: {h['question']}</div><div class='a'>{h['answer']}</div></div>")
    st.markdown("<div class='history-wrap'>" + "".join(cards) + "</div>", unsafe_allow_html=True)

def main():
    setup_ui()

if __name__ == "__main__":
    main()