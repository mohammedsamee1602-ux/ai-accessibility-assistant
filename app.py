"""Streamlit interface for the AI Accessibility Assistant."""

from io import BytesIO

import streamlit as st
from gtts import gTTS
from PIL import Image

from src.ocr import extract_text, preprocess_image
from src.text_processing import clean_ocr_text, text_to_braille


st.set_page_config(
    page_title="AI Accessibility Assistant",
    page_icon="♿",
    layout="wide",
)

st.title("♿ AI Accessibility Assistant")
st.write(
    "Extract text from an image, improve its readability and convert it into "
    "speech or Braille. Processing results are shown honestly—if OCR is not "
    "available, the application reports the error instead of returning demo data."
)

with st.sidebar:
    st.header("Accessibility settings")
    large_text = st.toggle("Larger interface text")
    high_contrast = st.toggle("High contrast")
    language = st.selectbox("OCR language", ["eng", "spa", "fra", "deu"])
    preprocess = st.toggle("Improve image before OCR", value=True)

if large_text:
    st.markdown("<style>html, body, [class*='css'] {font-size: 1.1rem;}</style>", unsafe_allow_html=True)
if high_contrast:
    st.markdown(
        "<style>.stApp {background:#000;color:#fff}.stButton button{border:2px solid #fff}</style>",
        unsafe_allow_html=True,
    )

upload_tab, camera_tab = st.tabs(["Upload an image", "Use the camera"])

image = None
source_name = "captured-image"

with upload_tab:
    uploaded_file = st.file_uploader(
        "Choose an image containing text",
        type=["png", "jpg", "jpeg", "bmp", "tiff", "webp"],
    )
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        source_name = uploaded_file.name.rsplit(".", 1)[0]

with camera_tab:
    captured_file = st.camera_input("Photograph a document, label or sign")
    if captured_file:
        image = Image.open(captured_file).convert("RGB")

if image is None:
    st.info("Upload or capture an image to begin.")
    st.stop()

left, right = st.columns(2)
with left:
    st.subheader("Source image")
    st.image(image, use_container_width=True)

if st.button("Extract text", type="primary", use_container_width=True):
    with st.spinner("Reading the image..."):
        try:
            result = extract_text(image, language=language, preprocess=preprocess)
            st.session_state["ocr_result"] = result
        except Exception as exc:
            st.session_state.pop("ocr_result", None)
            st.error(f"OCR could not run: {exc}")

result = st.session_state.get("ocr_result")
if result:
    with right:
        st.subheader("OCR result")
        metric_a, metric_b = st.columns(2)
        metric_a.metric("Average confidence", f"{result.confidence:.1f}%")
        metric_b.metric("Processing time", f"{result.processing_seconds:.2f}s")

        cleaned_text = clean_ocr_text(result.text)
        edited_text = st.text_area("Extracted text", cleaned_text, height=260)

        if not edited_text.strip():
            st.warning("No readable text was detected. Try a clearer, well-lit image.")
        else:
            st.download_button(
                "Download text",
                edited_text,
                file_name=f"{source_name}-extracted.txt",
                mime="text/plain",
                use_container_width=True,
            )

    if edited_text.strip():
        speech_tab, braille_tab = st.tabs(["Text to speech", "Braille output"])

        with speech_tab:
            speech_language = st.selectbox("Speech language", ["en", "es", "fr", "de"])
            slow_speech = st.toggle("Slower speech")
            if st.button("Generate audio"):
                try:
                    audio_buffer = BytesIO()
                    gTTS(edited_text, lang=speech_language, slow=slow_speech).write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    st.audio(audio_buffer.read(), format="audio/mp3")
                except Exception as exc:
                    st.error(f"Audio could not be generated: {exc}")

        with braille_tab:
            braille = text_to_braille(edited_text)
            st.text_area("Unicode Braille", braille, height=180)
            st.caption("This is Grade 1 Unicode Braille, intended as a learning aid rather than a certified transcription.")
