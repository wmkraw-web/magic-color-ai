import streamlit as st
import requests
import urllib.parse

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Magic Color AI", page_icon="🎨", layout="centered")

# --- INICJALIZACJA PAMIĘCI SESJI ---
if 'free_uses' not in st.session_state:
    st.session_state.free_uses = 0
if 'current_image_url' not in st.session_state:
    st.session_state.current_image_url = None
if 'current_image_data' not in st.session_state:
    st.session_state.current_image_data = None
if 'last_translated_prompt' not in st.session_state:
    st.session_state.last_translated_prompt = ""

MAX_FREE_USES = 3

# --- NAGŁÓWEK ---
st.title("🎨 Magic Color AI")
st.markdown("#### Inteligentny Generator Kolorowanek dla Dzieci")
st.write("Wpisz, co chcesz zobaczyć na kolorowance, a sztuczna inteligencja narysuje to w zaledwie 3 sekundy!")

# --- KONTROLA DOSTĘPU (PREMIUM) ---
st.sidebar.header("🔒 Odblokuj Magię (PRO)")
access_code = st.sidebar.text_input("Podaj kod Premium:", type="password")

is_premium = False
if access_code.upper() == "KAWA2024":
    is_premium = True
    st.sidebar.success("Kod poprawny! Nielimitowane generowanie odblokowane. 🎉")
elif access_code:
    st.sidebar.error("Nieprawidłowy kod. Postaw kawę autorowi, aby zdobyć dożywotni dostęp!")
    
st.sidebar.markdown("---")
st.sidebar.markdown("**Jak to działa?**")
st.sidebar.write(f"Każdy użytkownik może wygenerować {MAX_FREE_USES} darmowe kolorowanki na próbę.")
st.sidebar.markdown("[☕ Postaw Kawę, aby otrzymać kod nielimitowany!](https://buycoffee.to/magiccolor)")

# --- GŁÓWNY INTERFEJS ---
prompt_input = st.text_area("O czym ma być kolorowanka?", placeholder="np. Sowa w okularach czytająca książkę, wesoły dinozaur w kosmosie...", height=100)

age_group = st.selectbox(
    "Poziom trudności (wiek dziecka):",
    ["👶 Przedszkole (3-5 lat) - Grube kontury, bardzo proste", 
     "🧒 Wczesnoszkolne (6-8 lat) - Standardowe", 
     "👦 Starsze dzieci (9-12 lat) - Mnóstwo detali"]
)

# Informacja o limitach
if not is_premium:
    pozostalo = MAX_FREE_USES - st.session_state.free_uses
    if pozostalo > 0:
        st.info(f"🎁 Pozostało Ci darmowych generacji: **{pozostalo} z {MAX_FREE_USES}**")
    else:
        st.error("🛑 Wykorzystałeś swój darmowy limit! Podaj kod Premium w panelu po lewej stronie, aby rysować bez ograniczeń.")

button_disabled = (not is_premium) and (st.session_state.free_uses >= MAX_FREE_USES)

if st.button("✨ Generuj Kolorowankę", type="primary", use_container_width=True, disabled=button_disabled):
    if not prompt_input.strip():
        st.warning("Wpisz najpierw, co ma być na kolorowance!")
    else:
        with st.spinner("Sztuczna Inteligencja szkicuje dla Ciebie... ⏳"):
            try:
                # 1. NIEZAWODNE TŁUMACZENIE (Google Translate API)
                translated_prompt = prompt_input
                try:
                    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=pl&tl=en&dt=t&q={urllib.parse.quote(prompt_input)}"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        translated_prompt = data[0][0][0]
                except Exception as e:
                    pass # W razie skrajnej awarii wyśle polski tekst
                
                st.session_state.last_translated_prompt = translated_prompt

                # 2. Pobieranie klucza FAL z sejfu
                fal_key = st.secrets.get("FAL_KEY")
                if not fal_key:
                    st.error("Błąd Konfiguracji: Brak klucza FAL_KEY w ustawieniach (Secrets) Twojej aplikacji Streamlit!")
                    st.stop()

                headers = {
                    "Authorization": f"Key {fal_key}",
                    "Content-Type": "application/json"
                }
                
                # 3. Dostosowanie stylów wiekowych
                if "3-5" in age_group:
                    style_modifier = "very simple, extra thick bold black outlines, minimal details, easy to color for toddlers"
                elif "6-8" in age_group:
                    style_modifier = "clear black outlines, moderate details, standard coloring book style"
                else:
                    style_modifier = "highly detailed, intricate patterns, fine thin black outlines, advanced coloring page"

                # 4. MOCNY PROMPT (Skupienie na głównym temacie)
                full_prompt = f"A coloring page of: {translated_prompt}. {style_modifier}. Strictly black and white line art, pure solid white background, completely uncolored, crisp black lines, absolutely no shading, no grayscale, flat 2d vector."
                
                payload = {
                    "prompt": full_prompt,
                    "image_size": "portrait_4_3", 
                    "num_inference_steps": 4,     
                    "num_images": 1,
                    "enable_safety_checker": True
                }

                # Strzał do prywatnego serwera FAL.ai
                response = requests.post("https://fal.run/fal-ai/flux/schnell", headers=headers, json=payload, timeout=20)
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data["images"][0]["url"]
                    
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        st.session_state.current_image_url = image_url
                        st.session_state.current_image_data = img_response.content
                        
                        if not is_premium:
                            st.session_state.free_uses += 1
                            
                        st.rerun()
                    else:
                        st.error("Udało się wygenerować obrazek, ale nie można go pobrać na ekran.")
                else:
                    st.error(f"Błąd serwera generującego obrazek. Treść: {response.text}")

            except Exception as e:
                st.error(f"Wystąpił nieoczekiwany błąd aplikacji: {e}")

# --- SEKCJA WYŚWIETLANIA WYNIKÓW ---
if st.session_state.current_image_url and st.session_state.current_image_data:
    st.success("Gotowe! Oto Twoja unikalna kolorowanka:")
    st.image(st.session_state.current_image_url, use_container_width=True)
    
    # Wyświetlanie tłumaczenia dla pełnej kontroli
    st.caption(f"*(AI narysowało to na podstawie tłumaczenia: \"{st.session_state.last_translated_prompt}\")*")
    
    st.download_button(
        label="💾 Pobierz Kolorowankę (Gotowa do druku)",
        data=st.session_state.current_image_data,
        file_name="gotowa_kolorowanka.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

st.write("---")
st.caption("Pamiętaj: Wygenerowane grafiki są całkowicie unikalne, nie posiadają praw autorskich i możesz je swobodnie drukować i rozdawać dzieciom na zajęciach.")
