import streamlit as st
import easyocr
from transformers import pipeline
from PIL import Image
import requests
import io
import os

# Interfaz de usuario
st.title("📄 OCR + LLM en Facturas")
st.write("Sube una factura y extraeremos el **total, fecha y emisor**, además de una descripción con un LLM.")

# Entrada API Key de Hugging Face
hf_token = st.text_input("🔑 Ingresa tu API Key de Hugging Face:", type="password")

# Cargar imagen
uploaded_file = st.file_uploader("Sube una factura (imagen)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and hf_token:
    image = Image.open(uploaded_file)

    # OCR con EasyOCR
    reader = easyocr.Reader(["es", "en"])
    result = reader.readtext(image)

    extracted_text = " ".join([res[1] for res in result])
    st.subheader("📑 Texto extraído:")
    st.write(extracted_text)

    # LLM de Hugging Face
    generator = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", token=hf_token)
    prompt = f"""
    A partir del siguiente texto de una factura:
    ---
    {extracted_text}
    ---
    Resume indicando:
    - Emisor de la factura
    - Fecha de emisión
    - Total facturado
    """

    with st.spinner("🤖 Analizando con LLM..."):
        response = generator(prompt, max_length=300, do_sample=True)[0]["generated_text"]

    st.subheader("📋 Información estructurada con LLM:")
    st.write(response)
