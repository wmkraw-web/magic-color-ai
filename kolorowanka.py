import streamlit as st
import requests
import urllib.parse

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Magic Color AI", page_icon="🎨", layout="centered")

# --- NAGŁÓWEK ---
st.title("🎨 Magic Color AI")
st.markdown("#### Inteligentny Generator Kolorowanek dla Dzieci")
st.write("Wpisz, co chcesz zobaczyć na kolorowance, a sztuczna inteligencja narysuje to w zaledwie 3 sekundy!")

# --- KONTROLA DOSTĘPU (PREMIUM) ---
st.sidebar.header("🔒 Odblokuj Magię")
access_code = st.sidebar.text_input("Podaj kod Premium:", type="password")

is_premium = False
# Nasz ustalony tajny kod dostępu
if access_code.upper() == "KAWA2024":
    is_premium = True
    st.sidebar.success("Kod poprawny! Funkcje PRO odblokowane.")
elif access_code:
    st.sidebar.error("Nieprawidłowy kod. Postaw kawę autorowi, aby zdobyć dostęp!")
    
st.sidebar.markdown("[☕ Postaw Kawę, aby otrzymać kod](https://buycoffee.to/magiccolor)")

# --- GŁÓWNY INTERFEJS ---
prompt_input = st.text_area("O czym ma być kolorowanka?", placeholder="np. Wesoły dinozaur lecący rakietą w kosmos, sowa w okularach czytająca książkę...", height=100)

if st.button("✨ Generuj Kolorowankę", type="primary", use_container_width=True):
    if not is_premium:
        st.warning("Ta funkcja generuje koszty serwerowe. Wymaga podania kodu Premium w panelu po lewej stronie.")
    elif not prompt_input.strip():
        st.warning("Wpisz najpierw, co ma być na kolorowance!")
    else:
        with st.spinner("Sztuczna Inteligencja szkicuje dla Ciebie... (To potrwa około 3-4 sekund) ⏳"):
            try:
                # 1. Tłumaczenie na język angielski (Lepsze zrozumienie przez AI)
                translated_prompt = prompt_input
                try:
                    trans_url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(prompt_input)}&langpair=pl|en"
                    trans_res = requests.get(trans_url, timeout=5)
                    if trans_res.status_code == 200:
                        trans_data = trans_res.json()
                        if trans_data and "responseData" in trans_data and "MYMEMORY WARNING" not in trans_data["responseData"]["translatedText"]:
                            translated_prompt = trans_data["responseData"]["translatedText"]
                except Exception as e:
                    pass # Jeśli tłumacz zawiedzie, system użyje polskiego tekstu

                # 2. Pobieranie tajnego hasła z sejfu Streamlit
                fal_key = st.secrets.get("FAL_KEY")
                if not fal_key:
                    st.error("Błąd Konfiguracji: Brak klucza FAL_KEY w ustawieniach (Secrets) Twojej aplikacji Streamlit!")
                    st.stop()

                headers = {
                    "Authorization": f"Key {fal_key}",
                    "Content-Type": "application/json"
                }
                
                # Dodajemy modyfikatory zmuszające AI do zrobienia czystej kolorowanki
                full_prompt = f"{translated_prompt}, black and white coloring page for kids, line art, simple outlines, pure white background, no shading, monochrome"
                
                payload = {
                    "prompt": full_prompt,
                    "image_size": "portrait_4_3", # Kolorowanki idealnie pasują w formacie pionowym na kartkę A4
                    "num_inference_steps": 4,     # Magia wersji Schnell - błyskawiczne generowanie
                    "num_images": 1,
                    "enable_safety_checker": True
                }

                # Strzał do prywatnego, płatnego serwera FAL.ai
                response = requests.post("https://fal.run/fal-ai/flux/schnell", headers=headers, json=payload, timeout=20)
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data["images"][0]["url"]
                    
                    st.success("Gotowe! Oto Twoja unikalna kolorowanka:")
                    st.image(image_url, use_container_width=True)
                    
                    # Przycisk do pobierania gotowego obrazka
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        st.download_button(
                            label="💾 Pobierz Kolorowankę (Gotowa do druku)",
                            data=img_response.content,
                            file_name=f"kolorowanka_{prompt_input[:10].replace(' ', '_')}.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                else:
                    st.error(f"Błąd serwera generującego obrazek. Kod: {response.status_code}. Treść: {response.text}")

            except Exception as e:
                st.error(f"Wystąpił nieoczekiwany błąd aplikacji: {e}")

st.write("---")
st.caption("Pamiętaj: Wygenerowane grafiki są całkowicie unikalne, nie posiadają praw autorskich i możesz je swobodnie drukować i rozdawać dzieciom na zajęciach.")
