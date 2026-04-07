from groq import generate_response

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

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) <10:
        return True
    
    t = text.strip()

    if t.endswith(("**", "*", "-", ":", "(", "[", "{")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):
        return True
    if not re.search(r"[.!?](['\"])?\s*$", t):
        return True
    return False

def export_bytes(history):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i,h in enumerate(history, 1)])
    return io.BytesIO(text.encode("utf-8"))

def complete_answer(q: str, max_r: int = 2) -> str:
    base_prompt = f"""
        Answer clearly
        Do not cut sentences. Finish each point fully.
        Answer this Question: {q}
    """

    ans = generate_response(base_prompt, temp=0.3, max_tokens=1024)

    rounds = 0
    while rounds < max_r and looks_incomplete(ans):
        followup_prompt = f"""
            Continue the answer to the following question. Do not repeat what has already been said. Answer in numbered points and do not cut sentences.\n\n
            Question: {q}\n\nCurrent Answer: {ans}\n\nContinue the answer:
        """
        more = generate_response(followup_prompt, temp=0.3, max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = ans.strip() + "\n" + more.strip()
        rounds += 1
    return ans.strip()

def setup_ui():
    st.set_page_config(page_title="AI Teaching Assistant", page_icon=":robot_face:", layout="centered")
    st.title("AI Teaching Assistant")
    st.write("Welcome! You can ask me any question related to the course material, and I'll do my best to provide a clear and complete answer. If my initial response is incomplete, I'll automatically continue until I provide a full answer.")
    st.session_state.setdefault("history", [])

    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        ask = st.button("🚀 Ask")

    with col2:
        if st.button("🧹 Clear"):
            st.session_state.history = []
            st.rerun()

    with col3:
        if st.session_state.history:
            st.download_button(
                label="⬇ Export",
                data=export_bytes(st.session_state.history),
                file_name="qa_history.txt",
                mime="text/plain"
            )
        
    user_input = st.text_area("💬 Ask anything...", height=120)
    if ask:
        q = user_input.strip()
        if q:
            with st.spinner("Generating answer..."):
                a = complete_answer(q, 4)
            st.session_state.history.insert(0, {"question": q, "answer": a})
            st.rerun()
        
        else:
            st.warning("Please enter a question before asking.")

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