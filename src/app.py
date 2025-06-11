import streamlit as st
import requests
from PIL import Image

# 🔗 Ngrok Backend URL
BACKEND_URL = "https://5a66-35-192-211-198.ngrok-free.app/process"  # Change if needed

# ---------- Sidebar Content ----------
st.sidebar.title("📘 About Dialekt")
st.sidebar.markdown("""
**Dialekt** is a lightweight tool designed to help Tunisians understand signs and documents in French or Arabic — quickly translated into the Tunisian dialect.

🧩 **Solves**  
Foreign-language signs → Local understanding

🛠 **Stack**  
EasyOCR, Tesseract, Python, Colab, Streamlit

🚀 **Next Goals**
- ✅ Voice output in Tunisian  
- ✅ ML-based smarter translation  
- ⏳ PDF and form support  
""")
st.sidebar.markdown("---")
st.sidebar.caption("💡 Tip: Use light mode for cleanest view.")

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
        height: 320px !important;
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

# ---------- Expandable: About the Project ----------
with st.expander("📘 About the Project"):
    st.markdown("""
### 🎯 Inspiration
During a hackathon, we noticed a real issue — most signs and forms in Tunisia are in French or Arabic, making them hard for locals to understand. So we built a simple tool that lets users upload an image and get it translated to plain Tunisian dialect.

---

### 🛠 How We Built It
- **OCR Engine**: Tesseract for Arabic and French recognition  
- **Translator**: Rule-based converter for Tunisian expressions  
- **Backend**: Google Colab + Ngrok  
- **Frontend**: Streamlit  
- **Style**: Pure CSS for minimal, clean UI  

---

### 🚧 Challenges
- Poor image quality breaks OCR  
- Tunisian dialect lacks a formal structure, so translation had to be manual  
- Limited time meant keeping things extremely lightweight  
- Streamlit customization is basic — required CSS hacks  

---

### ✅ Accomplishments
- Upload → Extract → Translate in one smooth flow  
- Fully online — no local setup needed  
- Clean, non-distracting UI  
- Lightweight and fast

---

### 🧠 What We Learned
- OCR’s real-world limitations  
- How to keep things user-focused and simple  
- Customizing Streamlit layout creatively  
- Value of small, focused MVPs  

---

### 📌 What’s Next:
- ✅ Add voice output for the translated text  
- ✅ Improve dialect translation using ML  
- ✅ Support for PDFs, legal forms  
- ✅ Mobile-friendly UI and packaging as a PWA  

""")
