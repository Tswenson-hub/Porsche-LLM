import streamlit as st
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)
from main import complete_llm
import os


try:

    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
        SystemMessage(content="you are a helpful AI assistant. Reply your answer in markdown format.")
    ]

    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Bot is typing ..."):
            answer = complete_llm(user_input)
            st.session_state.messages.append(AIMessage(content=answer.response))
    else:
        st.markdown("This LLM was rapidly deployed using Free and open-source Python modules. This \
                    simple model is trained on a PDF export from wikipedia for 911 Porsches. In an enterprise \
                    setting this could be trained on company contract, complex records, or large CSV datasets and \
                    interacted with in the same way.")
        st.info("Are Porsches showcased in movies and TV shows?")
        st.info("Tell me a fact about Porsche Carreras that I didn't know.")
        st.info("Do Porsches have a history in racing?")

    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
except:
    st.write("Input not accepted. Ask a more concise question.")


