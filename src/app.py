import streamlit as st
import requests
from PIL import Image
import io

# 🔗 Ngrok Backend URL
BACKEND_URL = "https://5a66-35-192-211-198.ngrok-free.app/process"  # Change if needed

# ---------- Sidebar Content ----------
st.sidebar.title("📘 About Dialekt")
st.sidebar.markdown("""
**Dialekt** is a small tool built for real-life help — especially for people who find it hard to read signs in French or Arabic.

🧩 **What it solves**  
Many signs are in foreign languages. We make them simple by converting them to **Tunisian dialect**.

⚙️ **Built with**  
- EasyOCR & Tesseract  
- Python + Streamlit + Colab  
- Light, fast and no setup mess

🚀 **What’s next**  
- Voice translation in Tunisian  
- Smarter ML-based translation  
- Support for PDFs and forms
""")
st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: Light mode gives the cleanest look")

# ---------- Custom CSS ----------
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f5f5;
    }
    .block-container {
        padding-top: 1rem;
    }
    .stButton>button, .stFileUploader>div {
        border-radius: 0px !important;
    }
    .stImage>div>img {
        border-radius: 0px !important;
        height: 320px;
        object-fit: contain;
    }
    .feature-box {
        background-color: #f7f7f7;
        padding: 15px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
    }
    .translation-box {
        background-color: #fff;
        padding: 15px;
        border: 1px solid #ccc;
        border-radius: 0px;
        font-family: monospace;
        margin-top: 10px;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("📄 Dialekt - Understand Signs Around You")

# ---------- Feature Section ----------
st.markdown("""
<div class="feature-box">
<b>What it does:</b><br>
Snap a photo of a sign, notice, or board — and Dialekt will read the text (French/Arabic) and show it in plain Tunisian dialect.
<br><br>
<b>Key Features:</b>
<ul>
  <li>🧠 Reads French & Arabic signs using OCR</li>
  <li>🌍 Converts to local Tunisian phrases</li>
  <li>📤 Upload & Translate in one step</li>
  <li>🎯 Works inside Google Colab — zero setup</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ---------- File Upload Section ----------
uploaded_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🔁 Translate to Tunisian"):
        with st.spinner("⏳ Processing..."):
            image_bytes = uploaded_file.getvalue()
            response = requests.post(
                BACKEND_URL,
                files={"image": ("image.png", image_bytes, uploaded_file.type)}
            )
            if response.status_code == 200:
                result = response.json()

                # ---------- Results ----------
                st.markdown(f'<div class="translation-box"><b>📝 Extracted Text:</b><br>{result.get("extracted", "N/A")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="translation-box"><b>🇹🇳 Tunisian Dialect:</b><br>{result.get("tunisian", "N/A")}</div>', unsafe_allow_html=True)

                st.markdown("### 🌍 Other Translations")
                for lang, trans in result.get("translations", {}).items():
                    st.markdown(f"**{lang}:**")
                    st.markdown(f'<div class="translation-box">{trans}</div>', unsafe_allow_html=True)
            else:
                st.error("❌ Error processing the image. Please try another one.")

