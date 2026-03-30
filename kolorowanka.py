import streamlit as st
import urllib.parse
import random

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Magic Color AI", page_icon="🎨", layout="centered")

# --- NAGŁÓWEK ---
st.title("Magic Color AI - Generator Kolorowanek 🎨")
st.write("Wpisz, co chcesz pokolorować, a sztuczna inteligencja przygotuje dla Ciebie gotowy kontur do druku! Aplikacja jest w 100% darmowa.")

# --- POLE WPROWADZANIA ---
prompt = st.text_input("Temat kolorowanki (np. Wesoły lisek w lesie, Księżniczka na zamku):")

# --- PRZYCISK GENEROWANIA ---
if st.button("Generuj Kolorowankę", type="primary"):
    if prompt:
        with st.spinner("Trwa rysowanie magii... To potrwa kilka sekund ⏳"):
            
            # 1. Magiczne słowa kluczowe wymuszające czarno-biały kontur (line art)
            # Używamy języka angielskiego dla silnika AI, bo radzi sobie z nim najlepiej
            full_prompt = f"{prompt}, black and white coloring page for kids, clean line art, simple outlines, no shading, pure white background, flat vector, coloring book style"
            
            # 2. Kodowanie tekstu do formatu URL (aby usunąć spacje i polskie znaki dla linku)
            encoded_prompt = urllib.parse.quote(full_prompt)
            
            # 3. Losowy seed (ziarno) - dzięki temu wpisując drugi raz to samo, otrzymamy inny obrazek!
            seed = random.randint(1, 1000000)
            
            # 4. Generowanie linku z darmowego API Pollinations
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
            
            # 5. Wyświetlenie obrazka na ekranie
            st.image(image_url, caption=f"Twoja kolorowanka: {prompt}", use_container_width=True)
            
            st.success("Gotowe! Kliknij na obrazek prawym przyciskiem myszy (lub przytrzymaj palcem na telefonie) i wybierz 'Zapisz grafikę jako...', aby pobrać i wydrukować.")
    else:
        st.warning("Najpierw wpisz temat kolorowanki w polu powyżej!")

# --- SEKCJA WSPARCIA (SUBTELNA) ---
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
