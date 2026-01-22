from config import HF_API
from PIL import Image
from io import BytesIO
import requests

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3-medium-diffusers"

def generate_image(prompt: str) -> Image.Image:
    headers = {
        "Authorization": f"Bearer {HF_API}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": 512,            
            "height": 512,          
            "num_inference_steps": 50, 
            "guidance_scale": 7.5,   
            "seed": 42             
        },
        "options": {
            "use_gpu": True          # if your environment supports GPU
        }
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


def main():
    print("Welcome to Text-to-Image Generation!")
    print("Type exit to quit the program..")
    while True:
        prompt = input("Enter your image description: ")
        if prompt.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break
        try:
            image = generate_image(prompt)
            image.show()
            save_option = input("Do you want to save the image? (y/n)").strip().lower()
            if save_option in ["y", "yes"]:
                filename = input("Enter a filename without the extension: ").strip() or "generated_image"
                filename = "".join(c for c in filename if c.isalnum() or c in ("_", "-")).rstrip()
                image.save(f"{filename}.png")
                print(f"Image saved as {filename}.png")
        except Exception as e:
            print("An error occurred: " + str(e))
            print("\n")

        print("-" * 80 + "\n")

if __name__ == "__main__":
    main()  