import base64
import sys
import time
import easyocr
from PIL import Image, ImageOps
from io import BytesIO

OCR_MAX_IMG_SIZE = 3_000_000
VISION_MAX_IMG_SIZE = 1_690_000  # ~1300x1300; DeepSeek downscales to this server-side
VISION_MAX_IMG_BYTES = 1_000_000  # keep the aggregate request under DeepSeek's 48 MiB body limit
DEEPSEEK_MAX_REQUEST_BYTES = 48 * 1024 * 1024  # DeepSeek request body limit (vision guide)


def get_image_mime(bytes_data):
    image_type = Image.open(BytesIO(bytes_data)).format
    mime_types = {
        'JPEG': 'image/jpeg',
        'JPG': 'image/jpeg',
        'PNG': 'image/png',
        'GIF': 'image/gif',
        'WEBP': 'image/webp',
    }
    return mime_types.get(image_type, 'application/octet-stream')


def _encode_jpeg(image, quality=85):
    if image.mode != "RGB":
        image = image.convert("RGB")
    byte_stream = BytesIO()
    image.save(byte_stream, format="JPEG", quality=quality)
    return byte_stream.getvalue()


def vision_payload_size(data_urls):
    return sum(len(data_url) for data_url in data_urls)


def uploaded_img_to_img_bytes(uploaded_files):
    img_bytes = []
    for uploaded_file in uploaded_files:
        # Read file as bytes
        bytes_data = uploaded_file.getvalue()
        # Remove EXIF and downscale so the base64 payload stays within DeepSeek's limits
        image = ImageOps.exif_transpose(Image.open(BytesIO(bytes_data)))
        width, height = image.size
        if width * height > VISION_MAX_IMG_SIZE:
            scaling_factor = (VISION_MAX_IMG_SIZE / (width * height)) ** 0.5
            image = image.resize((int(width * scaling_factor), int(height * scaling_factor)))
            bytes_data = _encode_jpeg(image)
            mime_type = "image/jpeg"
        elif len(bytes_data) > VISION_MAX_IMG_BYTES:
            bytes_data = _encode_jpeg(image)
            mime_type = "image/jpeg"
        else:
            mime_type = get_image_mime(bytes_data)
        # Encode to base64
        base64_string = base64.b64encode(bytes_data).decode('utf-8')
        # Create full base64 string with MIME type prefix
        full_base64_string = f"data:{mime_type};base64,{base64_string}"
        # Append base64_string to array of image bytes
        img_bytes.append(full_base64_string)
    return img_bytes


def _log(msg):
    print(f"[ocr] {msg}", file=sys.stderr, flush=True)


def uploaded_img_to_text(st_status, uploaded_files, lang = "en"):
    text = ""
    t_start = time.perf_counter()
    _log(f"start: {len(uploaded_files)} image(s), lang={lang}")
    reader = easyocr.Reader([lang])
    _log(f"reader ready in {time.perf_counter() - t_start:.1f}s")
    for i, uploaded_file in enumerate(uploaded_files, 1):
        st_status.update(label=f"Extracting text from {uploaded_file.name}...")
        t_img = time.perf_counter()
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
            image = image.resize((int(width * scaling_factor), int(height * scaling_factor)))
        # Convert image to an in-memory file (BytesIO)
        byte_stream = BytesIO()
        image.save(byte_stream, format='JPEG')
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
        _log(f"image {i}/{len(uploaded_files)} {uploaded_file.name}: {time.perf_counter() - t_img:.1f}s ({width}x{height}, {len(result)} regions)")
    _log(f"done: total {time.perf_counter() - t_start:.1f}s, {len(text)} chars")
    return text