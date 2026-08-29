# AI Accessibility Assistant

A Python and Streamlit application that extracts text from images and turns it into more accessible formats. Users can upload an image or capture one with a camera, run OCR, edit the extracted text, generate spoken audio and view a Grade 1 Unicode Braille representation.

## Why I built it

This project was developed as my final-year Computer Science project around assistive technology. The goal was to explore how OCR and speech technologies can reduce barriers when printed or visual text is difficult to access.

## Features

- Image upload and browser camera capture
- Tesseract OCR with average word-confidence reporting
- Optional grayscale, contrast and sharpening preprocessing
- Editable and downloadable OCR results
- Text-to-speech output using gTTS
- Grade 1 Unicode Braille conversion
- Larger-text and high-contrast interface options
- Automated tests for deterministic processing functions

## Technology

- Python
- Streamlit
- Tesseract OCR and pytesseract
- Pillow
- gTTS
- Pytest

## Architecture

```text
Image upload or camera
          ↓
Image preprocessing
          ↓
Tesseract OCR + confidence data
          ↓
Editable extracted text
       ↙       ↘
Text-to-speech  Braille output
```

## Run locally

### 1. Install Tesseract

Install Tesseract OCR for your operating system and confirm that this command works:

```bash
tesseract --version
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies and start the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run the tests

```bash
pytest
```

## Testing and limitations

OCR accuracy depends on image resolution, lighting, orientation, typography and the installed Tesseract language packs. The application reports measured confidence rather than claiming a fixed accuracy rate. gTTS requires an internet connection. The Braille feature provides a basic Grade 1 Unicode representation and is not a replacement for certified Braille transcription software.

## Project status

Portfolio version of a completed university prototype. Future improvements could include document layout preservation, offline speech generation and a larger OCR evaluation set.
