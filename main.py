import streamlit as st
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time

# Iniciar el servidor Ollama
# Nota: Asegúrate de que Ollama esté instalado y configurado correctamente
# Puedes ejecutar este comando en tu terminal antes de iniciar la aplicación
# !Ollama serve

llm = Ollama(model="llama3:8b")

def main():
    # Inyectar CSS personalizado para cambiar la estética
    st.markdown("""
    <style>
    /* Cambiar el color de fondo de la aplicación */
    .stApp {
        background-color: #000000; /* Negro */
        color: #00FF00; /* Verde */
    }
    
    /* Cambiar el color de los títulos */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #00FF00; /* Verde */
    }
    
    /* Cambiar el color de los botones */
    .css-1aumxhk button {
        background-color: #00FF00;
        color: #000000;
    }
    
    /* Cambiar el color de los campos de texto */
    .stTextInput>div>div>input {
        background-color: #333333;
        color: #00FF00;
    }
    
    /* Cambiar el color del área de texto */
    .stTextArea>div>div>textarea {
        background-color: #333333;
        color: #00FF00;
    }
    
    /* Cambiar el color de los spinner y otros elementos */
    .stSpinner {
        color: #00FF00;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("CircuitSage - Asistente Técnico")

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
        else:
            # Mostrar un mensaje de "espera" mientras se procesa la respuesta
            with st.spinner("Generando respuesta, por favor espera..."):
                start_time = time.time()
                response = chain.invoke({"input": user_input, "chat_history": st.session_state["chat_history"]})
                elapsed_time = time.time() - start_time
                if elapsed_time > 60:
                    st.warning("La generación de la respuesta está tardando más de lo esperado.")

            st.session_state["chat_history"].append(HumanMessage(content=user_input))
            st.session_state["chat_history"].append(AIMessage(content=response))

    chat_display = ""
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display += f"🦧Yo: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_display += f"🔧{bot_name}: {msg.content}\n"

    st.text_area("Chat", value=chat_display, height=400, key="chat_area")

if __name__ == '__main__':
    main()
