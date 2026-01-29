from config import HF_API
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import requests
import datetime
import os

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3-medium-diffusers"
TIMEOUT = 30
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_image(prompt: str) -> Image.Image:
    headers = {"Authorization": f"Bearer {HF_API}"}
    payload = {"inputs": prompt}

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=TIMEOUT
    )
    response.raise_for_status()

    if "image" not in response.headers.get("Content-Type", ""):
        raise Exception("Response is not an image")

    return Image.open(BytesIO(response.content)).convert("RGB")

def daylight_edition(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(1.25)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    return img.filter(ImageFilter.GaussianBlur(radius=0.8))

def night_mood(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(0.9)
    img = ImageEnhance.Contrast(img).enhance(1.4)
    return img.filter(ImageFilter.GaussianBlur(radius=1.3))

def save_image(img: Image.Image, name: str):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path)
    print(f"Saved: {path}")

def main():
    print("AI Image Generator | Type quit to exit")

    while True:
        prompt = input("\nEnter prompt: ").strip()
        if prompt.lower() == "quit":
            break

        try:
            print("Generating image...")
            base_image = generate_image(prompt)

            daylight = daylight_edition(base_image)
            night = night_mood(base_image)

            daylight.show()
            night.show()

            save = input("Save images? (y/n): ").lower()
            if save in ("y", "yes"):
                name = input("Filename prefix: ").strip() or "image"
                save_image(daylight, f"{name}_daylight")
                save_image(night, f"{name}_night")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
