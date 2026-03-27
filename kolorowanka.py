import streamlit as st
import os
import json
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from googletrans import Translator
from google.oauth2 import service_account

# --- 1. LOGIKA BEZPIECZNEGO KLUCZA ---
def get_creds():
    # Sprawdza czy jesteśmy na serwerze Streamlit (Secrets)
    if "google_credentials" in st.secrets:
        creds_dict = json.loads(st.secrets["google_credentials"])
        return service_account.Credentials.from_service_account_info(creds_dict)
    # Jeśli nie, szuka pliku lokalnie u Ciebie na dysku
    elif os.path.exists("klucz.json"):
        return service_account.Credentials.from_service_account_file("klucz.json")
    else:
        st.error("Brak klucza dostępu! (klucz.json lub Secrets)")
        return None

creds = get_creds()
PROJECT_ID = "decoded-reducer-449618-i7"

if creds:
    vertexai.init(project=PROJECT_ID, location="us-central1", credentials=creds)

# --- 2. USTAWIENIA STRONY I WYGLĄD ---
st.set_page_config(page_title="MagicColor AI", page_icon="🖍️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    h1 { color: #FF4B4B !important; text-align: center; font-size: 3rem !important; }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 10px; width: 100%; height: 3em; font-weight: bold; }
    .stDownloadButton>button { background-color: #28a745; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS ---
st.title("🖍️ MagicColor AI")
st.write("<p style='text-align: center;'>Twoje osobiste studio kolorowanek</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.text_area("Co narysować? (pisz po polsku)", placeholder="np. kotek w rakiecie")
    btn = st.button("🚀 GENERUJ")

with col2:
    if btn and user_input:
        with st.spinner("Rysuję..."):
            try:
                translator = Translator()
                eng_text = translator.translate(user_input, src='pl', dest='en').text
                
                model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                prompt = f"Coloring page for kids, {eng_text}, black and white, thick outlines, white background"
                
                response = model.generate_images(prompt=prompt, number_of_images=1)
                img_bytes = response.images[0]._image_bytes
                
                st.image(img_bytes, use_container_width=True)
                st.download_button("💾 POBIERZ PNG", img_bytes, f"kolorowanka.png", "image/png")
            except Exception as e:
                st.error(f"Błąd: {e}")
    else:
        st.info("Czekam na Twój pomysł...")