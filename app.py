import streamlit as st
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)
from main import complete_llm


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
    st.markdown("Can't think of anything? Try one of these prompts!")
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
