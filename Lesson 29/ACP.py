import os
import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from colorama import Fore, Style, init

init(autoreset=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_id = "nlpconnect/vit-gpt2-image-captioning"
model = VisionEncoderDecoderModel.from_pretrained(model_id).to(device)
processor = ViTImageProcessor.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

def caption_image(image_path, max_length, min_length=5):
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)

    output_ids = model.generate(
        pixel_values,
        max_length=max_length,
        min_length=min_length,
        num_beams=4

    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

def main():
    path = input("Enter image path: ").strip()

    if not os.path.isfile(path):
        print(Fore.RED + "Error: Invalid image path")
        return

    try:
        print(Fore.CYAN + "Generating basic caption...")
        basic_caption = caption_image(path, max_length=15)
        print(Fore.GREEN + "Caption:", basic_caption)

        choice = input(Fore.YELLOW + "Expand to ~30 words? (y/n): ").lower()

        if choice in ("y", "yes"):
            print(Fore.CYAN + "Generating expanded description...")
            long_caption = caption_image(path, max_length=35, min_length=25)
            print(Fore.GREEN + "Expanded Description:", long_caption)

    except Exception as e:
        print(Fore.RED + "Error:", e)

if __name__ == "__main__":
    main()
