from src.text_processing import clean_ocr_text, text_to_braille


def test_clean_ocr_text_preserves_paragraphs():
    source = " First   line\nsecond line\n\nNew paragraph "
    assert clean_ocr_text(source) == "First line second line\n\nNew paragraph"


def test_text_to_braille_converts_basic_letters():
    assert text_to_braille("abc!") == "⠁⠃⠉⠖"
