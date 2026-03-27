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
    # Najpierw szuka w Secrets (na serwerze)
    if "google_credentials" in st.secrets:
        creds_dict = json.loads(st.secrets["google_credentials"])
        return service_account.Credentials.from_service_account_info(creds_dict)
    # Jeśli nie ma, szuka pliku lokalnie (u Ciebie na komputerze)
    elif os.path.exists("klucz.json"):
        return service_account.Credentials.from_service_account_file("klucz.json")
    return None

creds = get_creds()
PROJECT_ID = "decoded-reducer-449618-i7"

if creds:
    vertexai.init(project=PROJECT_ID, location="us-central1", credentials=creds)

# --- 2. KONFIGURACJA STRONY ---
st.set_page_config(page_title="MagicColor AI", page_icon="🎨", layout="wide")

# Stylizacja CSS (Wygląd Premium)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    h1 { color: #FF4B4B !important; text-align: center; font-size: 3rem !important; margin-bottom: 0; font-family: 'Arial Black', sans-serif; }
    .coffee-btn {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #FFDD00;
        color: #000000 !important;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        text-decoration: none;
        margin-top: 10px;
        font-size: 1.1rem;
    }
    .stButton>button { background-color: #FF4B4B; color: white; border-radius: 10px; width: 100%; font-weight: bold; height: 3.5em; border: none; }
    .stDownloadButton>button { background-color: #28a745; color: white; border-radius: 10px; width: 100%; height: 3.5em; border: none; }
    .stSelectbox label, .stTextArea label { color: white !important; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PASEK BOCZNY (MENU) ---
st.sidebar.header("☕ Wsparcie")
# --- LINIA 51: TU WPISZ SWOJĄ NAZWĘ Z BUYCOFFEE ---
buy_coffee_url = "https://buycoffee.to/magiccolor" 
st.sidebar.markdown(f'<a href="{buy_coffee_url}" target="_blank" class="coffee-btn">🎁 Postaw mi kawę</a>', unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.info("Każda 'kawa' pozwala mi generować więcej darmowych kolorowanek dla dzieciaków! Dzięki!")

# --- 4. INTERFEJS GŁÓWNY ---
st.markdown("<h1 class='main-title'>🎨 MagicColor AI</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; font-size: 1.2rem;'>Zamień wyobraźnię w kolorowankę w kilka sekund!</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 📝 Co dziś rysujemy?")
    user_input = st.text_area(
        "Opisz pomysł (np. uśmiechnięty kotek w okularach przeciwsłonecznych):", 
        placeholder="Pisz śmiało po polsku...",
        height=120
    )
    
    style = st.selectbox("Wybierz styl rysunku:", [
        "Prosty (dla najmłodszych)", 
        "Bajkowy (piękne detale)", 
        "Realistyczny",
        "Mandala (relaksujący/trudny)"
    ])
    
    st.write("")
    generate_btn = st.button("🚀 GENERUJ KOLOROWANKĘ")

with col2:
    if generate_btn and user_input:
        if not creds:
            st.error("⚠️ Problem z połączeniem! Sprawdź klucz Google w Secrets.")
        else:
            with st.spinner("🪄 Magia w toku... Tłumaczę i przygotowuję styl..."):
                try:
                    # 1. Tłumaczenie
                    translator = Translator()
                    eng_text = translator.translate(user_input, src='pl', dest='en').text
                    
                    # 2. Dobieranie ulepszonych promptów
                    style_prompts = {
                        "Prosty (dla najmłodszych)": "very simple toddler coloring page, thick bold black outlines, large open spaces, white background, no interior detail, minimalistic, cute flat vector style",
                        "Bajkowy (piękne detale)": "enchanting storybook style coloring page, magical atmosphere, clean black line art, whimsical details, professional illustration, pure white background, high contrast",
                        "Realistyczny": "realistic line art coloring page, accurate proportions, detailed but clear outlines, nature-inspired, fine black ink drawing, white background",
                        "Mandala (relaksujący/trudny)": "intricate mandala coloring page, symmetrical patterns, geometric folk art, filled with zen ornaments, complex black and white line work, stress-relief style"
                    }
                    
                    final_prompt = f"Professional coloring book page, {eng_text}, {style_prompts[style]}, line art only, black and white, pure white background, no shading, no shadows, no colors, no gradients, clean edges"
                    
                    # 3. Generowanie obrazu
                    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
                    response = model.generate_images(prompt=final_prompt, number_of_images=1)
                    img_bytes = response.images[0]._image_bytes
                    
                    # 4. Wyświetlanie i pobieranie
                    st.image(img_bytes, caption=f"Twoja kolorowanka: {user_input}", use_container_width=True)
                    
                    st.download_button(
                        label="💾 POBIERZ I WYDRUKUJ (PNG)",
                        data=img_bytes,
                        file_name=f"kolorowanka_{user_input[:15]}.png",
                        mime="image/png"
                    )
                    st.success("Gotowe! Możesz teraz pobrać i wydrukować rysunek.")
                    
                except Exception as e:
                    st.error(f"Coś poszło nie tak: {e}")
    elif generate_btn and not user_input:
        st.warning("Musisz wpisać, co mam narysować!")
    else:
        st.markdown("### 🖼️ Podgląd")
        st.info("Wpisz pomysł po lewej i kliknij 'Generuj', aby zobaczyć magię!")

# Stopka
st.divider()
# --- 5. STOPKA I REGULAMIN ---
st.divider()
st.markdown("<p style='text-align: center; color: #888;'>MagicColor AI v1.5 | Wykorzystuje Google Imagen 3</p>", unsafe_allow_html=True)

with st.expander("⚖️ Regulamin i Polityka Prywatności"):
    st.write("""
    **1. O serwisie:** MagicColor AI to narzędzie demonstracyjne wykorzystujące sztuczną inteligencję Google do generowania kolorowanek.
    
    **2. Prywatność:** Nie zbieramy Twoich danych osobowych. Twoje opisy (prompty) są przesyłane do Google Cloud w celu wygenerowania obrazu. Nie przechowujemy Twoich zdjęć ani gotowych kolorowanek na naszym serwerze.
    
    **3. Prawa autorskie:** Wygenerowane kolorowanki są przeznaczone do użytku osobistego i domowego. Możesz je drukować dowolną ilość razy dla swoich dzieci.
    
    **4. Darowizny:** Przycisk 'Postaw mi kawę' jest dobrowolną darowizną na pokrycie kosztów serwerów AI i nie stanowi opłaty za konkretny produkt.
    
    **5. Odpowiedzialność:** AI może czasem wygenerować nietypowe kształty. Zawsze sprawdź rysunek przed podaniem go dziecku.
    """)