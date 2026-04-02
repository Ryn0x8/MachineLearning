import config
from openai import OpenAI

GROQ_URL = "https://api.groq.com/openai/v1"
MODELS = getattr(config, "GROQ_MODELS", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])

def generate_response(prompt: str, temp: float = 0.3, max_tokens :int = 512) -> str:
    key = getattr(config, "GROQ_API", None)
    if not key:
        return "Error: GROQ API key not found. Please set the GROQ_API variable in config.py."
    c = OpenAI(api_key=key, base_url=GROQ_URL)

    last_err = None
    for m in MODELS:
        try:
            r = c.chat.completions.create(
                model = m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            last_err = e

    return f"Error generating response: {last_err}. Please check your GROQ API key and model availability. OR Switch to huggingface"

