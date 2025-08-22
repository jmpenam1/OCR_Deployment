import streamlit as st
import easyocr
import re
from transformers import pipeline

# Título de la app
st.title("📄 OCR + LLM - Facturas Inteligentes")

# Campo para API Key de Hugging Face
api_key = st.text_input("🔑 Ingresa tu API Key de Hugging Face", type="password")

# Cargador de imagen
uploaded_file = st.file_uploader("Sube una foto de la factura", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    # Inicializar OCR
    reader = easyocr.Reader(['es', 'en'])
    results = reader.readtext(uploaded_file.read(), detail=0)

    # Concatenar el texto leído
    extracted_text = "\n".join(results)

    st.subheader("📝 Texto extraído:")
    st.text(extracted_text)

    # Extraer datos clave con regex simples
    total = re.search(r'(\$?\s?\d+[\.,]?\d{0,2})', extracted_text)
    fecha = re.search(r'(\d{2}[/-]\d{2}[/-]\d{2,4})', extracted_text)
    emisor = re.search(r'(?i)(?:emitido por|factura de|emisor[: ]+)([A-Za-z\s]+)', extracted_text)

    datos = {
        "total": total.group(1) if total else "No encontrado",
        "fecha": fecha.group(1) if fecha else "No encontrada",
        "emisor": emisor.group(1).strip() if emisor else "No encontrado"
    }

    st.subheader("📌 Datos clave encontrados:")
    st.json(datos)

    # Conectar con un LLM de Hugging Face
    generator = pipeline(
        "text-generation",
        model="tiiuae/falcon-7b-instruct",
        token=api_key
    )

    prompt = f"""
    Tengo una factura con la siguiente información extraída por OCR:
    - Total: {datos['total']}
    - Fecha: {datos['fecha']}
    - Emisor: {datos['emisor']}

    Por favor, genera una breve descripción en lenguaje natural.
    """

    try:
        response = generator(prompt, max_length=200, do_sample=True)
        descripcion = response[0]["generated_text"]

        st.subheader("🧠 Descripción generada por LLM:")
        st.write(descripcion)

    except Exception as e:
        st.error(f"Error al conectar con Hugging Face: {e}")

elif uploaded_file and not api_key:
    st.warning("⚠️ Ingresa tu API Key de Hugging Face para procesar con el LLM.")

