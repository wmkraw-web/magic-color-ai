import streamlit as st
import urllib.parse
import random
import requests

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Magic Color AI", page_icon="🎨", layout="centered")

# --- NAGŁÓWEK ---
st.title("Magic Color AI - Generator Kolorowanek 🎨")
st.write("Wpisz, co chcesz pokolorować, wybierz styl, a sztuczna inteligencja przygotuje gotowy kontur do druku! Aplikacja jest w 100% darmowa.")

# --- FORMULARZ ---
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_input("Temat kolorowanki (np. Wesoły lisek, Zamek księżniczki):")

with col2:
    style_choice = st.selectbox(
        "Wybierz styl i trudność:",
        [
            "👶 Dla maluchów (Bardzo proste)",
            "🎈 Dla przedszkolaków (Rysunkowe)",
            "🎒 Dla starszych (Realistyczne)",
            "🌀 Mandale (Wzory relaksacyjne)"
        ]
    )

# --- SŁOWNIK STYLÓW DLA AI ---
STYLE_PROMPTS = {
    "👶 Dla maluchów (Bardzo proste)": "very simple thick outlines, minimal details, bold line art, easy coloring page for toddlers, no background clutter",
    "🎈 Dla przedszkolaków (Rysunkowe)": "cute cartoon style, clear outlines, coloring book page for kids, friendly, clean background",
    "🎒 Dla starszych (Realistyczne)": "detailed realistic line art, intricate outlines, educational coloring page, realistic proportions",
    "🌀 Mandale (Wzory relaksacyjne)": "intricate symmetrical mandala pattern, zen tangle style, highly detailed circular line art, adult coloring book page"
}

# --- PRZYCISK GENEROWANIA ---
if st.button("Generuj Kolorowankę", type="primary", use_container_width=True):
    if prompt:
        with st.spinner("Trwa rysowanie magii (włączono tryb Turbo)... ⏳"):
            
            selected_style_modifier = STYLE_PROMPTS[style_choice]
            base_rules = "pure black and white coloring page, clean line art, absolutely no shading, no grayscale, pure white background, flat 2d vector"
            
            if "Mandale" in style_choice:
                full_prompt = f"{prompt} integrated into an {selected_style_modifier}, {base_rules}"
            else:
                full_prompt = f"{prompt}, {selected_style_modifier}, {base_rules}"
            
            encoded_prompt = urllib.parse.quote(full_prompt)
            seed = random.randint(1, 1000000)
            
            # NOWOŚĆ: Dodano &model=flux dla ekstremalnej szybkości!
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
            
            try:
                # NOWOŚĆ: Przedstawiamy się jako prawdziwa przeglądarka (User-Agent), aby ominąć blokadę
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                response = requests.get(image_url, headers=headers, timeout=60)
                
                # Sprawdzamy czy na pewno pobraliśmy obrazek (a nie stronę błędu)
                if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                    st.image(response.content, caption=f"Twoja kolorowanka: {prompt} ({style_choice})", use_container_width=True)
                    st.success("Gotowe! Kliknij na obrazek prawym przyciskiem myszy (lub przytrzymaj palcem na telefonie) i wybierz 'Zapisz grafikę jako...', aby pobrać i wydrukować.")
                else:
                    st.error("Serwer AI zablokował zapytanie lub jest przeciążony. Spróbuj kliknąć Generuj jeszcze raz!")
            
            except Exception as e:
                st.error("Wystąpił błąd pobierania obrazka. Sprawdź połączenie z internetem i spróbuj ponownie.")
    else:
        st.warning("Najpierw wpisz temat kolorowanki w polu powyżej!")

# --- SEKCJA WSPARCIA ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
    <h3 style='color: #4a4a4a; margin-bottom: 10px;'>💡 Podoba Ci się to narzędzie?</h3>
    <p style='color: #6c757d; font-size: 14px;'>
        Utrzymanie moich aplikacji generuje spore koszty. Zdecydowałem się jednak zostawić kolorowanki <b>całkowicie za darmo</b>.<br>
        Jeśli ta aplikacja oszczędziła Ci trochę czasu i wywołała uśmiech u dzieci, możesz symbolicznie wesprzeć moją pracę.
    </p>
    <a href="https://buycoffee.to/magiccolor" target="_blank" style="text-decoration: none;">
        <button style='background-color: #f59e0b; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px;'>
            ☕ Postaw mi wirtualną kawę
        </button>
    </a>
</div>
""", unsafe_allow_html=True)
