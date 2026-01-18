from config import HF_API
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3-medium-diffusers"

def generate_image(prompt: str) -> Image.Image:
    headers = {
        "Authorization": f"Bearer {HF_API}"
    }
    payload = {
        "inputs": prompt
    }
    try:
        response = requests.post(API_URL, headers = headers, json = payload, timeout = 30)
        response.raise_for_status()
        if 'image' in response.headers.get('Content-Type', ''):
            image = Image.open(BytesIO(response.content))
            return image
        else:
            raise Exception("The response is not an image. It might be an error")
    except requests.exceptions.RequestException as e:
        raise Exception("Request Failed: " + str(e))

def postprocess_image(img):
    enhancer = ImageEnhance.Brightness(img)
    brighted = enhancer.enhance(1.2)

    enhancer = ImageEnhance.Contrast(brighted)
    contrasted = enhancer.enhance(1.3)

    soft_focus_image = contrasted.filter(ImageFilter.GaussianBlur(radius = 1))

    return soft_focus_image

def main():
    print("Welcome to AI Enhanced Image Generator")
    print("This program generates and image from text and post process it")
    print("Type quit to exit")
    while True:
        user_input = input("Enter the description of image you want to generate: ")
        if user_input.lower() == "quit":
            break
        try:
            print("\nGenerating Image....")
            generated_image = generate_image(user_input)
            print("Post Processing Image.....")
            processed = postprocess_image(generated_image)
            processed.show()
            save_option = input("Do you want to save the image? (y/n)").strip().lower()
            if save_option in ["y", "yes"]:
                filename = input("Enter a filename without the extension: ").strip() or "generated_image"
                filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-")).rstrip()
                processed.save(f"{filename}.png")
                print(f"Image saved as {filename}.png")
        except Exception as e:
            print("An error has occured: " + str(e))
        print("*" * 80)
        print("\n\n")

if __name__ == "__main__":
    main()
    
