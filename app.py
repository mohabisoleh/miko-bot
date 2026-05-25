import streamlit as st
import google.generativeai as genai
from openai import OpenAI  # Impor library OpenAI untuk DALL-E 3

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Miko: Si Teman Produktif", page_icon="💼", layout="centered")

# --- Ambil API Key secara aman dari Secrets Streamlit ---
gemini_key = st.secrets["GEMINI_API_KEY"]
openai_key = st.secrets["OPENAI_API_KEY"]

# --- Inisialisasi Klien AI ---
try:
    # Koneksi ke Gemini (Otak Teks)
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-pro') 

    # Koneksi ke OpenAI (Tangan Gambar DALL-E 3)
    openai_client = OpenAI(api_key=openai_key)
except Exception:
    st.error("Waduh, ada kendala koneksi ke otak AI Miko. Cek API Key di Secrets, ya!")
    gemini_model = None
    openai_client = None

# --- Inisialisasi Riwayat Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat di layar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], caption=msg.get("caption"))
        else:
            st.write(msg["content"])

# --- Proses Input Chat dari User ---
if user_input := st.chat_input("Tanya Miko apa saja..."):
    # Tampilkan chat user di layar
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "type": "text"})

    # Respon dari Miko
    with st.chat_message("assistant"):
        input_lower = user_input.lower()
        
        # --- FITUR DETEKSI PERINTAH GAMBAR ---
        if "buat gambar" in input_lower or "bikin gambar" in input_lower or "buat foto" in input_lower:
            with st.spinner("Miko lagi ambil kuas dan menggambar buat kamu... 🎨"):
                try:
                    # Bersihkan keyword agar DALL-E fokus pada objek gambarnya saja
                    prompt_gambar = user_input.replace("buat gambar", "").replace("bikin gambar", "").replace("buat foto", "").strip()
                    
                    # Panggil DALL-E 3
                    response = openai_client.images.generate(
                        model="dall-e-3",
                        prompt=prompt_gambar,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    
                    # Ambil URL hasil gambar
                    url_gambar = response.data[0].url
                    
                    # Tampilkan gambar di chat Streamlit
                    st.image(url_gambar, caption=f"Hasil gambar: {prompt_gambar}")
                    
                    # Simpan ke riwayat chat sebagai tipe image
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": url_gambar, 
                        "type": "image", 
                        "caption": prompt_gambar
                    })
                except Exception as e:
                    st.error(f"Aduh maaf sayang, Miko gagal menggambar: {e}")
        
        # --- FITUR CHAT TEKS BIASA (GEMINI) ---
        else:
            with st.spinner("Miko lagi mikir..."):
                try:
                    # Jalankan perintah teks lewat Gemini seperti biasa
                    response = gemini_model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text, "type": "text"})
                except Exception as e:
                    st.error(f"Ada kendala koneksi ke otak Gemini Miko: {e}")
