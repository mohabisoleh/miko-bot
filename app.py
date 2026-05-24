import streamlit as st
from google import genai

st.set_page_config(page_title="Miko: Si Teman Produktif", page_icon="💼", layout="centered")

# --- PASANG KUNCI API KAMU DI SINI ---
API_KEY = "AIzaSyBytv4A8yMAoMtpws8Gon2pU__eMMDxkNk"

# Inisialisasi Otak Google AI
try:
    client = genai.Client(api_key=API_KEY)
except Exception:
    client = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! 💼 Aku Miko, asisten produktivitas pribadimu yang baru di-upgrade dengan otak AI! Sekarang kamu bisa tanya apa saja, curhat, atau minta jadwal belajar ke aku. Yuk tulis di bawah! ✨"}
    ]
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

with st.sidebar:
    st.header("📝 Catatan Tugas Hari Ini")
    input_tugas = st.text_input("Tambah tugas baru:")
    if st.button("Tambah"):
        if input_tugas:
            st.session_state.todo_list.append(input_tugas)
            st.rerun()
            
    if st.session_state.todo_list:
        st.write("Daftar Tugasmu:")
        for i, tugas in enumerate(st.session_state.todo_list):
            st.write(f"{i+1}. {tugas}")
        if st.button("Hapus Semua Tugas"):
            st.session_state.todo_list = []
            st.rerun()
    else:
        st.caption("Belum ada tugas yang dicatat. Yuk tulis di atas!")

st.title("💼 Miko: Si Teman Produktif (AI Mode)")
st.caption("Asisten AI Pintar untuk Mengatur Jadwal, Tugas, dan Motivasi Belajar")
st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_query := st.chat_input("Tanya Miko apa saja..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Miko sedang berpikir keras... 🧠"):
            if client and API_KEY != "PASTE_KUNCI_API_KAMU_DI_SINI":
                try:
                    prompt_instruksi = f"Kamu adalah Miko, asisten produktivitas, belajar, dan motivasi yang ramah, seru, dan suportif. Jawablah chat ini dengan gaya Miko: {user_query}"
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_instruksi,
                    )
                    bot_response = response.text
                except Exception as e:
                    bot_response = f"Aduh maaf sayang, ada kendala koneksi ke otak AI-ku nih: {str(e)}"
            else:
                bot_response = "Kunci API AI-ku belum dimasukkan dengan benar di kodingan, sayang. Cek baris nomor 7 ya!"

            st.write(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})