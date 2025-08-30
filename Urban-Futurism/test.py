import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
from PIL import Image

img = Image.open("NUM_PLATE.jpg")

text = pytesseract.image_to_string(img)

print(text)