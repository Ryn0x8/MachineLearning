from io import BytesIO
import requests
import streamlit as st
from huggingface_hub import InferenceClient

import config

MODEL_ID = "stabilityai/stable-diffusion-3-medium-diffusers"
FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"

ENHANCE_SYS = (
    "Improve prompt for text-to-image. Return only the enhanced prompt",
    "Add subject, style, lighting, camera angle, background, colors. Keep it safe"
)

NEGATIVE = "low quality, blurry, deformed, bad anatomy, disfigured, poorly drawn, extra limbs, close up, b&w, weird colors, text, watermark, cropped, distorted"

img_client = InferenceClient(provider="hf-inference", token=config.HF_API)

def check_prompt_with_filter_api(prompt: str):
    try:
        response = requests.post(
            FILTER_API_URL,
            json={"prompt": prompt},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            return {"ok": False, "error": "Invalid response format from filter API"}
        return data
    except Exception as e:
        return {"ok": False, "reason": "Filter API error: " + str(e)}
    
def enhance_prompt(prompt: str) -> str:
    from groq import generate_response
    out = generate_response(
        f"{ENHANCE_SYS}\nUSER PROMPT: {prompt}",
        temp=0.4,
        max_tokens=220
    )
    return (out or prompt).strip()

def gen_image(prompt: str):
    filter_res = check_prompt_with_filter_api(prompt)
    if not filter_res.get("ok", False):
        return None, "Prompt rejected by filter: " + filter_res.get("reason", "Unknown reason")
    
    try:
        return img_client.text_to_image(
            prompt = prompt,
            negative_prompt = NEGATIVE,
            model = MODEL_ID,
        ), None
    except Exception as e:
        msg = str(e)
        if "negative_prompt" in msg or "unexpected keyword" in msg:
            try:
                return img_client.text_to_image(
                    prompt = prompt,
                    model = MODEL_ID,
                ), None
            except Exception as e2:
                msg = str(e2)

        if any(x in msg for x in ["402", "Payment Required", "pre-paid credits"]):
            return None, "Model is currently unavailable due to resource constraints. Please try again later. RAW ERROR: " + msg
        
        if "404" in msg or "Not Found" in msg:
            return None, "Model not found. Please check the MODEL_ID and your HuggingFace API access. RAW ERROR: " + msg
        
        return None, "Error generating image: " + msg
    
def main():
    st.set_page_config(page_title="AI Art Studio", page_icon=":art:", layout="centered")
    st.title("Safe AI Image Generator")
    st.info("Flow: Enter prompt -> Enhance -> Filter Check -> Generate Image. If your prompt is rejected, try rephrasing it.")

    with st.form("img_form", clear_on_submit=True):
        raw = st.text_area(
            "Image description prompt",
            height = 120,
            placeholder="e.g., A serene landscape with mountains, a river, and a sunset in the background, in the style of impressionism",
        )
        submit = st.form_submit_button("Generate Image")
        if submit:
            raw = raw.strip()
            if not raw:
                st.warning("Please enter a image description")
                return
            
            raw_check = check_prompt_with_filter_api(raw)
            if not raw_check.get("ok", False):
                st.error("Your original prompt was rejected by our safety filter: " + raw_check.get("reason", "Unknown reason"))
                return
            
            with st.spinner("Enhancing prompt..."):
                final_prompt = enhance_prompt(raw)
            
            enhanced_check = check_prompt_with_filter_api(final_prompt)
            if not enhanced_check.get("ok", False):
                st.error("The enhanced prompt was rejected by our safety filter: " + enhanced_check.get("reason", "Unsafe prompt"))
                return
            
            st.markdown("### Enhanced Prompt")
            st.code(final_prompt)

            with st.spinner("Generating image..."):
                img, err = gen_image(final_prompt)
                if err:
                    st.error(err)
                    return
                
                st.image(img, caption="Generated Image", use_container_width=True)
                st.session_state.generated_image = img

    img = st.session_state.get("generated_image", None)
    if img:
        buf = BytesIO()
        img.save(buf, format = "PNG")
        st.download_button(
            label="Download Image",
            data=buf.getvalue(),
            file_name="AI_GENERATED_IMG.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()


            
            