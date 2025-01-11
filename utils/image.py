import imghdr
import base64
import easyocr
from PIL import Image, ImageOps
from io import BytesIO

OCR_MAX_IMG_SIZE = 3_000_000


def get_image_mime(file):
    image_type = imghdr.what(file)
    mime_types = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
    }
    return mime_types.get(image_type, 'application/octet-stream')


def uploaded_img_to_img_bytes(uploaded_files):
    img_bytes = []
    for uploaded_file in uploaded_files:
        # Read file as bytes
        bytes_data = uploaded_file.getvalue()
        # Identify image type and get MIME type
        mime_type = get_image_mime(uploaded_file)
        # Encode to base64
        base64_string = base64.b64encode(bytes_data).decode('utf-8')
        # Create full base64 string with MIME type prefix
        full_base64_string = f"data:{mime_type};base64,{base64_string}"
        # Append base64_string to array of image bytes
        img_bytes.append(full_base64_string)
    return img_bytes


def uploaded_img_to_text(uploaded_files, lang):
    text = ""
    reader = easyocr.Reader([lang])
    for uploaded_file in uploaded_files:
        # Convert bytes to an image
        image = Image.open(uploaded_file)
        # Remove EXIF from image
        image = ImageOps.exif_transpose(image)
        # Get image dimensions
        width, height = image.size
        # Resize image if it's too large
        if width * height > OCR_MAX_IMG_SIZE:
            scaling_factor = (OCR_MAX_IMG_SIZE / (width * height)) ** 0.5
            # Resize image using scaling_factor
            image_small = image.resize((int(width * scaling_factor), int(height * scaling_factor)))
            # Convert the smaller image to an in-memory file (BytesIO)
            byte_stream = BytesIO()
            image_small.save(byte_stream, format='JPEG')
            byte_stream.seek(0)
            image = byte_stream.getvalue()
        # Extract text using EasyOCR
        result = reader.readtext(image)
        # Extract text from result
        page = " ".join([res[1] for res in result])
        # Adding page to text
        text += page
        # Adding page separator
        text += "\n---\n"
    return text