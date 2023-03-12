from PIL import Image
from pytesseract import pytesseract

# Define path to tesseract
image = Image.open('sample-image/clash.png')

text = pytesseract.image_to_string(image)
print(text)

# count = text.count("the")
# print(f"{count}")