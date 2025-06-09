import base64
import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None


# Path to your image
image_path = r"C:\Users\isaac\PycharmProjects\pictures2obsdian\scripts\20250309_095812.jpg"
image_path = r"C:\Users\isaac\PycharmProjects\pictures2obsdian\scripts\20250309_095801.jpg"
image_path = r"C:\Users\isaac\PycharmProjects\pictures2obsdian\scripts\WhatsApp Image 2025-06-08 at 9.51.05 PM.jpeg"
image_path = r"C:\Users\isaac\PycharmProjects\pictures2obsdian\scripts\Screenshot 2025-06-08 220922.png"
# image_path = r"C:\Users\isaac\PycharmProjects\pictures2obsdian\scripts\math.png"

# Getting the base64 string
base64_image = encode_image(image_path)

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{base64_image}"
    },
    include_image_base64=True
)
# %%
text = ocr_response.pages[0].markdown

print(text)
# %%


def write_image(path, base64_string):
    with open(path, "wb") as image_file:
        if base64_string.startswith("data:image"):
            base64_string = base64_string.split(",")[1]
        image_file.write(base64.b64decode(base64_string))


for image in ocr_response.pages[0].images:
    image_path=image.id
    base64_string=image.image_base64
    print(image_path)
    write_image(rf"C:\Users\isaac\PycharmProjects\pictures2obsdian\scripts\{image_path}",
                base64_string)
