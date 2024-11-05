import streamlit as st
from openai import OpenAI

# Título y descripción
st.title("💬 Chatbot")
st.write("Este es un chatbot que utiliza diferentes modelos GPT")

# Lista de modelos disponibles
model_options = ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4", "gpt-4o","gpt-4o-mini"]
selected_model = st.selectbox("Selecciona un modelo GPT", model_options)

# Obtener la API Key correspondiente al modelo seleccionado
try:
    openai_api_key = st.secrets[selected_model]
except KeyError:
    st.error(f"No se encontró una API Key para el modelo {selected_model}.")
    st.stop()

# Crear un cliente OpenAI
client = OpenAI(api_key=openai_api_key)

# Inicializar mensajes en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada de chat
if prompt := st.chat_input("¿En qué te puedo ayudar?"):
    # Almacenar y mostrar el prompt actual
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar una respuesta utilizando el modelo seleccionado
    stream = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Mostrar la respuesta en el chat y almacenarla
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
