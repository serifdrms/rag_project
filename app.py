import streamlit as st
from rag import ask

st.set_page_config(page_title="AI İçerik Uyum Danışmanı", page_icon="🤖")

st.title("🤖 AI İnfluencer Uyum Danışmanı")
st.markdown("Instagram ve TikTok kuralları hakkında sorularını sor!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sorunuzu yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            response = ask(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})