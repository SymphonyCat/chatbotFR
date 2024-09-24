import streamlit as st
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
from pydantic import ValidationError
import requests

# Cambia esta dirección por la URL pública de ngrok o Localtunnel cuando lo uses
SERVER_URL = "http://<tu-ngrok-id>.ngrok.io"  # Cambia esto

# Intentar inicializar el modelo con manejo de errores
try:
    llm = Ollama(model="llama3:8b", server_url=SERVER_URL)  # Usa SERVER_URL
except ValidationError as e:
    st.error(f"Error de validación: {e.json()}")
    st.stop()  # Detener la ejecución si hay un error de validación
except Exception as e:
    st.error(f"Error al inicializar el modelo: {str(e)}")
    st.stop()  # Detener la ejecución si hay otro tipo de error

def main():
    st.title("CircuitSage-Asistente Técnico")

    bot_name = "CircuitSage"
    bot_description = f"""Eres un asistente virtual especializado en resolver problemas técnicos de laptops y computadoras de sobremesa solamente. Te llamas {bot_name}, respondes preguntas con respuestas detalladas. Además, debes preguntar al usuario acorde al contexto del chat, y también preguntar al usuario para obtener una respuesta más detallada, pero solamente te presentaras con un hola y preguntando al usuario que se le ofrece o cual es su problema, cualquier tema que no este relacionada con el hardware de las computadoras y laptops descartalo y hacelo saber al usuario de forma contundente."""

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt_template | llm

    user_input = st.text_input("Escribe tu pregunta:", key="user_input")

    if st.button("Enviar"):
        if user_input.lower() == "adios":
            st.stop()
        elif user_input.strip():
            with st.spinner("Generando respuesta, por favor espera..."):
                start_time = time.time()
                try:
                    response = chain.invoke({"input": user_input, "chat_history": st.session_state["chat_history"]})
                    st.session_state["chat_history"].append(HumanMessage(content=user_input))
                    st.session_state["chat_history"].append(AIMessage(content=response))
                except Exception as e:
                    st.error("Error al generar la respuesta. Asegúrate de que Ollama está funcionando correctamente.")
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
