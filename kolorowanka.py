import streamlit as st
import os
import json
import io
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from googletrans import Translator
from google.oauth2 import service_account

# --- 1. BEZPIECZNE LOGOWANIE (SECRETS LUB PLIK) ---
def get_creds():
    if "google_credentials" in st.secrets:
        creds_dict = json.loads(st.secrets["google_credentials"])
        return service_account.Credentials.from_service_account_info(creds_dict)
    elif os.path.exists("klucz.json"):
        return service_account.Credentials.from_service_account_file("klucz.json")
    return None

creds = get_creds()
PROJECT_ID = "decoded-reducer-449618-i7"

if creds:
    vertexai.init(project=PROJECT_ID, location="us-central1", credentials=creds)

# --- 2. KONFIGURACJA STRONY ---
st.set_page_config(page_title="MagicColor AI", page_icon="🎨", layout="wide")

# Stylizacja CSS (Dark Mode + Wyraźne przyciski)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    h1 { color: #FF4B4B !important; text-align: center; font-size: 3rem !important; margin-bottom: 0; }
    .coffee-btn {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #FFDD00;
        color: #000000 !important;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
        text-decoration: none;
        margin-top: 10px;
    }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    .stDownloadButton>button { background-color: #28a745; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INTERFEJS ---
st.title("https://buycoffee.to/magiccolor")
st.write("<p style='text-align: center;'>Twoje studio unikalnych kolorowanek</p>", unsafe_allow_html=True)

# Przycisk Kawy (Wpisz swój link poniżej!)
st.sidebar.header("Wesprzyj projekt")
buy_coffee_url = "https://buycoffee.to/twoja-nazwa" # <--- TU WPISZ SWÓJ LINK
st.sidebar.markdown(f'<a href="{buy_coffee_url}" target="_blank" class="coffee-btn">☕ Postaw mi kawę</a>', unsafe_allow_html=True)
st.sidebar.write("Dzięki Tobie mogę rozwijać to narzędzie!")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🖍️ Stwórz rysunek")
    user_input = st.text_area("Co narysować? (np. lwa w koronie)", height=100)
    
    # WYBÓR STYLU
    style = st.selectbox("Wybierz styl kolorowanki:", [
        "Prosty (dla maluchów)", 
        "Bajkowy (dużo detali)", 
        "Realistyczny",
        "Mandala (trudny)"
    ])
    
    generate_btn = st.button("🚀 GENERUJ MAGICZNIE")

with col2:
    if generate_btn and user_input:
        if not creds:
            st.error("Błąd klucza Google! Sprawdź Secrets.")
        else:
            with st.spinner("Tłumaczę i przygotowuję styl..."):
                try:
                    # Tłumaczenie
                    translator = Translator()
                    eng_text = translator.translate(user_input, src='pl', dest='en').text
                    
                    # Dobieranie promptu do stylu
                    style_prompts = {
                        "Prosty (dla maluchów)": "very simple, thick bold black outlines, white background, no details, for 3 year olds",
                        "Bajkowy (dużo detali)": "fairytale style, cute, detailed black and white line art, professional outlines",
                        "Realistyczny": "realistic proportions, clean black lines, detailed but paintable, white background",
                        "Mandala (trudny)": "mandala style patterns inside, intricate geometric details, black and white"
                    }
                    
                    final_prompt = f"Coloring page for kids, {eng_text}, {style_prompts[style]}, pure white background, black ink only"
                    
                    # Generowanie
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    response = model.generate_images(prompt=final_prompt, number_of_images=1)
                    img_bytes = response.images[0]._image_bytes
                    
                    # Wynik
                    st.image(img_bytes, caption=f"Styl: {style}", use_container_width=True)
                    st.download_button("💾 POBIERZ I DRUKUJ", img_bytes, "kolorowanka.png", "image/png")
                    st.success("Gotowe! Nie zapomnij się pochwalić!")
                    
                except Exception as e:
                    st.error(f"Coś poszło nie tak: {e}")
    else:
        st.info("Podaj pomysł po lewej, aby zacząć.")

st.divider()
st.caption("MagicColor AI 2026 | Twórz, drukuj, koloruj!")