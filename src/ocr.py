"""OCR operations and image preprocessing."""

from dataclasses import dataclass
from time import perf_counter

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
from pytesseract import Output


@dataclass(frozen=True)
class OCRResult:
    text: str
    confidence: float
    processing_seconds: float


def preprocess_image(image: Image.Image) -> Image.Image:
    """Return a grayscale, contrast-enhanced image suitable for OCR."""
    grayscale = ImageOps.grayscale(image)
    enhanced = ImageEnhance.Contrast(grayscale).enhance(1.6)
    return enhanced.filter(ImageFilter.SHARPEN)


def _mean_confidence(data: dict) -> float:
    values = []
    for raw_value in data.get("conf", []):
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            continue
        if value >= 0:
            values.append(value)
    return sum(values) / len(values) if values else 0.0


def extract_text(
    image: Image.Image,
    language: str = "eng",
    preprocess: bool = True,
) -> OCRResult:
    """Extract text and average word confidence from a PIL image."""
    source = preprocess_image(image) if preprocess else image.convert("RGB")
    started = perf_counter()
    text = pytesseract.image_to_string(source, lang=language).strip()
    data = pytesseract.image_to_data(source, lang=language, output_type=Output.DICT)
    elapsed = perf_counter() - started
    return OCRResult(text=text, confidence=_mean_confidence(data), processing_seconds=elapsed)
