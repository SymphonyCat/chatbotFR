import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time


llm = Ollama(model="llama3:8b")

def main():
    st.title("CircuitSage-Asistente Técnico")

    bot_name = "CircuitSage"
    bot_description = f"""Eres un asistente virtual especializado en resolver problemas técnicos de laptops y computadoras de sobremesa solamente. Te llamas {bot_name}, respondes preguntas con respuestas detalladas. Además, debes preguntar al usuario acorde al contexto del chat y también preguntar al usuario para obtener una respuesta más detallada. Solo te presentarás con un hola y preguntando al usuario qué se le ofrece o cuál es su problema. Cualquier tema que no esté relacionado con el hardware de las computadoras y laptops descártalo de forma contundente."""

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

    chat_display = "\n".join(
        f"🦧Yo: {msg.content}" if isinstance(msg, HumanMessage) else f"🔧{bot_name}: {msg.content}"
        for msg in st.session_state["chat_history"]
    )

    st.text_area("Chat", value=chat_display, height=400, key="chat_area", disabled=True)

if __name__ == '__main__':
    main()
