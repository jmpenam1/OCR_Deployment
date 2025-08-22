import streamlit as st
import pytesseract
from PIL import Image
import cv2
import requests
import os

# -----------------------------
# Configuración inicial
# -----------------------------
st.set_page_config(page_title="Factura OCR + LLM", page_icon="🧾", layout="centered")

st.title("🧾 Asistente de Facturas con OCR + LLM")

# Ingreso de API Key de Hugging Face
hf_api_key = st.text_input("🔑 Ingresa tu Hugging Face API Key", type="password")

# -----------------------------
# Subida de imagen
# -----------------------------
uploaded_file = st.file_uploader("📤 Sube la foto de la factura", type=["jpg", "jpeg", "png"])

if uploaded_file and hf_api_key:
    # Leer imagen
    image = Image.open(uploaded_file)
    st.image(image, caption="Factura cargada", use_column_width=True)

    # Convertir a escala de grises y aplicar OCR
    img_cv = cv2.cvtColor(cv2.imread(uploaded_file.name), cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img_cv, lang="spa")

    st.subheader("📑 Texto detectado (OCR):")
    st.text(text)

    # -----------------------------
    # Llamada a LLM en Hugging Face
    # -----------------------------
    st.subheader("🤖 Resumen del LLM:")

    headers = {"Authorization": f"Bearer {hf_api_key}"}
    llm_model = "mistralai/Mistral-7B-Instruct-v0.2"  # se puede cambiar por otro modelo
    api_url = f"https://api-inference.huggingface.co/models/{llm_model}"

    prompt = f"""
    A partir del siguiente texto extraído de una factura, identifica:
    - Emisor
    - Fecha
    - Total
    Luego genera una breve descripción de la factura en lenguaje natural.
    
    Texto OCR:
    {text}
    """

    with st.spinner("Consultando al modelo..."):
        response = requests.post(api_url, headers=headers, json={"inputs": prompt})
        
        if response.status_code == 200:
            output = response.json()
            # Hugging Face puede devolver texto en distintos formatos
            try:
                llm_text = output[0]["generated_text"]
            except:
                llm_text = output
            st.write(llm_text)
        else:
            st.error(f"Error en la API: {response.status_code} - {response.text}")
