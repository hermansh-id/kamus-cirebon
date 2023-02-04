import streamlit as st
from main import translate
st.title("Kamus Bahasa Cerbon")

mode = st.selectbox("Mode", ["cerbon", "bebasan"])
text = st.text_area("Input Text")

mulai = st.button("Mulai")

if (text != "") and mulai:
    hasil = translate(text, mode)
    st.header("Hasil :")
    st.write(hasil)