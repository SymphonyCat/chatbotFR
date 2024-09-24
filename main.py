import streamlit as st
import requests
import time
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Cambia esta dirección por la URL pública de ngrok o Localtunnel cuando lo uses
SERVER_URL = "http://<tu-ngrok-id>.ngrok.io"  # Cambia esto

def generate_response(user_input, chat_history):
    payload = {
        "input": user_input,
        "chat_history": chat_history
    }
    response = requests.post(f"{http://127.0.0.1:4040 }/api/chat", json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No se recibió respuesta.")
    else:
        raise Exception("Error en la comunicación con el servidor.")

def main():
    st.title("CircuitSage-Asistente Técnico")

    bot_name = "CircuitSage"
    bot_description = "Eres un asistente virtual especializado en resolver problemas técnicos..."

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    user_input = st.text_input("Escribe tu pregunta:", key="user_input")

    if st.button("Enviar"):
        if user_input.lower() == "adios":
            st.stop()
        elif user_input.strip():
            with st.spinner("Generando respuesta, por favor espera..."):
                start_time = time.time()
                try:
                    response = generate_response(user_input, st.session_state["chat_history"])
                    st.session_state["chat_history"].append(HumanMessage(content=user_input))
                    st.session_state["chat_history"].append(AIMessage(content=response))
                except Exception as e:
                    st.error("Error al generar la respuesta.")
                    st.error(str(e))
                elapsed_time = time.time() - start_time
                if elapsed_time > 60:
                    st.warning("La generación de la respuesta está tardando más de lo esperado.")
        else:
            st.warning("Por favor, escribe un mensaje antes de enviar.")

    chat_display = ""
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display += f"🦧Yo: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_display += f"🔧{bot_name}: {msg.content}\n"

    st.text_area("Chat", value=chat_display, height=400, key="chat_area")

if __name__ == '__main__':
    main()
