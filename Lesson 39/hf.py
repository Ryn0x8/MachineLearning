import config
from huggingface_hub import InferenceClient

MODELS = getattr(config, "HF_MODELS", ["meta-llama/Llama-3.1-8B-Instruct"])


def generate_response(prompt: str, temp: float = 0.3, max_tokens :int = 512) -> str:
    key = getattr(config, "HF_API", None)
    if not key:
        return "Error: HuggingFace API key not found. Please set the HF_API variable in config.py."

    last_err = None
    for m in MODELS:
        try:
            c = InferenceClient(token=key, model=m)
            r = c.chat_completion(
                model = m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err = e

    return f"Error generating response: {last_err}. Please check your GROQ API key and model availability. OR Switch to huggingface. Tried Models: {', '.join(MODELS)}"

