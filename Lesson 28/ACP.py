import os
import torch
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
OUTPUT_FILE = "captions_summary.txt"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
).to(device)

processor = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

tokenizer = AutoTokenizer.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning"
)

def generate_caption(image: Image.Image) -> str:
    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)

    output_ids = model.generate(
        pixel_values,
        max_length=20,
        num_beams=4
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

def main():
    folder = input("Enter image folder path: ").strip()

    if not os.path.isdir(folder):
        print("Invalid folder path")
        return

    image_files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(IMAGE_EXTENSIONS)
    ]

    if not image_files:
        print("No valid images found")
        return

    results = []

    for filename in image_files:
        try:
            path = os.path.join(folder, filename)
            image = Image.open(path).convert("RGB")
            caption = generate_caption(image)
            results.append(f"{filename}: {caption}")
            print(f"Captioned: {filename}")
        except Exception as e:
            results.append(f"{filename}: ERROR - {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"\nCaptions saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
