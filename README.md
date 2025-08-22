# 📄 Extractor de Datos de Facturas

Este proyecto es un **prototipo en Streamlit** que permite subir una **foto de una factura** y extraer automáticamente los siguientes campos:

- 🏢 **Emisor**  
- 📅 **Fecha**  
- 💰 **Total**

El sistema utiliza **OCR (Reconocimiento Óptico de Caracteres)** con [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) y expresiones regulares para identificar información clave en el texto.

---

## 🚀 Demo rápida

1. Ejecuta la aplicación con Streamlit.  
2. Sube una imagen de una factura (`.jpg`, `.jpeg`, `.png`).  
3. Visualiza el texto detectado y los campos extraídos.  

---

## 📦 Requisitos

### Dependencias de Python

Instala las librerías necesarias con:

```bash
pip install -r requirements.txt
