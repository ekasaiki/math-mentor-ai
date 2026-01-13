from PIL import Image
import pytesseract

def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)

    confidence = 0.9 if text.strip() else 0.3
    return text.strip(), confidence
