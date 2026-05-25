import streamlit as st
import google.generativeai as genai
from openai import OpenAI

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Miko: Si Teman Produktif", page_icon="💼", layout="centered")

# --- Inisialisasi Klien ---
# Pastikan kamu sudah isi Secrets di dashboard Streamlit
try:
    gemini_key = st.secrets["GEMINI_API_KEY"]
    openai_key = st.secrets["OPENAI_API_KEY"]
    
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    openai_client = OpenAI(api_key=openai_key)
except Exception as e:
    st.error(f"Error Konfigurasi: {e}")
    st.stop() # Ini akan menghentikan proses jika kunci API belum diset

# --- Riwayat Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"], caption=msg.get("caption"))
        else:
            st.write(msg["content"])

# --- Chat Input ---
if user_input := st.chat_input("Tanya Miko apa saja..."):
    st.session_state.messages.append({"role": "user", "content": user_input, "type": "text"})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        input_lower = user_input.lower()
        
        # Fitur Gambar
        if any(k in input_lower for k in ["buat gambar", "bikin gambar", "buat foto"]):
            with st.spinner("Miko lagi menggambar..."):
                try:
                    prompt = user_input.replace("buat gambar", "").replace("bikin gambar", "").replace("buat foto", "").strip()
                    response = openai_client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1)
                    url = response.data[0].url
                    st.image(url)
                    st.session_state.messages.append({"role": "assistant", "content": url, "type": "image", "caption": prompt})
                except Exception as e:
                    st.error(f"Gagal gambar: {e}")
        
        # Fitur Chat
        else:
            with st.spinner("Miko lagi mikir..."):
                try:
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text, "type": "text"})
                except Exception as e:
                    st.error(f"Error Gemini: {e}")
