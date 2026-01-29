from PIL import Image
import os
from colorama import Fore, init, Style
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

MODEL_ID = "nlpconnect/vit-gpt2-image-captioning"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NUM_BEAMS = 5

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
feature_extractor = ViTImageProcessor.from_pretrained(MODEL_ID)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_ID)

tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.eos_token_id
model.config.eos_token_id = tokenizer.eos_token_id
model.to(DEVICE)
model.eval()

init(autoreset=True)

# --------- Helpers ---------
def query_hf_api(image_paths, GEN_KWARGS):
    images = []
    for path in image_paths:
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    pixel_values = feature_extractor(
        images=images,
        return_tensors="pt"
    ).pixel_values.to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(pixel_values, **GEN_KWARGS)

    captions = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    return [c.strip() for c in captions]

def truncate_by_words(text, max_words):
    words = text.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "…"
    return text

def print_menu():
    print(f"""{Style.BRIGHT}
==Image to Text Generation==
1. Generate Caption (5 words)
2. Generate Summary (50 words)
3. Generate Description (20 words)
4. Exit
""")

def main():
    image_paths = [input("Enter the image path for Image to Text Generation: ")]
    if not all([os.path.exists(p) for p in image_paths]):
        print(Fore.RED + "One or more image paths are invalid. Please check and try again.")
        return

    FULL_GEN_KWARGS = {
        "max_length": 80,     
        "num_beams": NUM_BEAMS,
        "repetition_penalty": 1.2,
        "early_stopping": True,
        "no_repeat_ngram_size": 2,
        "min_length": 50
    }
    full_texts = query_hf_api(image_paths, FULL_GEN_KWARGS)

    while True:
        print_menu()
        choice = input("Select an option (1-4): ")

        for i, full_text in enumerate(full_texts):
            if choice == "1":  
                print(f"Image {i+1} Caption (5 words): {truncate_by_words(full_text, 5)}")
            elif choice == "2":  
                print(f"Image {i+1} Summary (50 words): {truncate_by_words(full_text, 50)}")
            elif choice == "3":  
                print(f"Image {i+1} Description (20 words): {truncate_by_words(full_text, 20)}")
        if choice == "4":
            print("Exiting...")
            break
        elif choice not in ["1", "2", "3"]:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
