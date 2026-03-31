import streamlit as st
import urllib.parse
import random
import streamlit.components.v1 as components

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
        selected_style_modifier = STYLE_PROMPTS[style_choice]
        base_rules = "pure black and white coloring page, clean line art, absolutely no shading, no grayscale, pure white background, flat 2d vector"
        
        if "Mandale" in style_choice:
            full_prompt = f"{prompt} integrated into an {selected_style_modifier}, {base_rules}"
        else:
            full_prompt = f"{prompt}, {selected_style_modifier}, {base_rules}"
        
        encoded_prompt = urllib.parse.quote(full_prompt)
        seed = random.randint(1, 1000000)
        
        # Link do AI z szybkim modelem
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}&model=flux"
        
        # --- MAGIA HTML/JS: Aplikacja już się nie zawiesza. Wrzucamy ładowanie na barki przeglądarki! ---
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; padding: 10px; background-color: #ffffff; }}
                #image-container {{ position: relative; display: inline-block; width: 100%; max-width: 800px; min-height: 350px; border: 2px dashed #cbd5e1; border-radius: 16px; padding: 20px; background-color: #f8fafc; transition: all 0.3s; }}
                img {{ max-width: 100%; height: auto; border-radius: 8px; display: none; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); margin: 0 auto; }}
                .loader {{ 
                    border: 5px solid #e2e8f0; border-top: 5px solid #4f46e5; border-radius: 50%; 
                    width: 50px; height: 50px; animation: spin 1s linear infinite;
                    margin: 60px auto 20px auto;
                }}
                @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                .btn-group {{ margin-top: 25px; display: none; gap: 15px; justify-content: center; }}
                .btn {{ padding: 14px 28px; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; }}
                .btn-print {{ background-color: #4f46e5; color: white; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3); }}
                .btn-down {{ background-color: #10b981; color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); }}
                .btn:hover {{ transform: translateY(-3px); opacity: 0.9; box-shadow: 0 6px 15px rgba(0,0,0,0.15); }}
                
                /* Ukryj przyciski i ramki podczas samego drukowania */
                @media print {{
                    .btn-group, #loading-text {{ display: none !important; }}
                    #image-container {{ border: none; padding: 0; width: 100%; max-width: none; background-color: transparent; }}
                    img {{ width: 100%; max-height: 98vh; object-fit: contain; display: block !important; box-shadow: none; }}
                    body {{ padding: 0; margin: 0; }}
                }}
            </style>
        </head>
        <body>
            <div id="image-container">
                <div id="loading-text">
                    <div class="loader"></div>
                    <h3 style="color: #1e293b; margin-bottom: 5px; font-size: 20px;">Sztuczna Inteligencja rysuje... 🎨</h3>
                    <p style="color: #64748b; font-size: 14px; line-height: 1.5;">To skomplikowany proces, który może zająć <b>od 5 do 30 sekund</b>.<br>Obrazek pojawi się tutaj automatycznie. Proszę o cierpliwość!</p>
                </div>
                <img id="kolorowanka" src="{image_url}" alt="Kolorowanka" crossorigin="anonymous" onload="showImage()">
            </div>

            <div id="buttons" class="btn-group">
                <button class="btn btn-print" onclick="window.print()">🖨️ Wydrukuj bezpośrednio</button>
                <button class="btn btn-down" onclick="downloadImage()">💾 Pobierz na komputer</button>
            </div>

            <script>
                // Funkcja wywoływana automatycznie, gdy obrazek się pobierze
                function showImage() {{
                    document.getElementById('loading-text').style.display = 'none';
                    document.getElementById('kolorowanka').style.display = 'block';
                    document.getElementById('image-container').style.border = 'none';
                    document.getElementById('image-container').style.backgroundColor = 'transparent';
                    document.getElementById('buttons').style.display = 'flex';
                }}

                // Funkcja pobierania
                async function downloadImage() {{
                    const img = document.getElementById('kolorowanka');
                    try {{
                        const response = await fetch(img.src);
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = url;
                        a.download = 'kolorowanka.png';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }} catch (e) {{
                        // Opcja zapasowa, gdyby serwer zablokował pobieranie w tle
                        const a = document.createElement('a');
                        a.href = img.src;
                        a.download = 'kolorowanka.png';
                        a.target = '_blank';
                        a.click();
                    }}
                }}
            </script>
        </body>
        </html>
        """
        # Wyświetlamy nasz nowy, sprytny moduł w aplikacji (wysokość 900px, by zmieścił przyciski i obrazek)
        components.html(html_code, height=900, scrolling=False)
        
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
