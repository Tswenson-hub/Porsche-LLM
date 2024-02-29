import streamlit as st
import pandas as pd
import os

st.title("LLAMA.INDEX RAG + PORSCHE")
st.markdown(
    "Checkout this cool project built using the LLAMA.INDEX modules freely available via Python.\
      This demonstrates how easy it is to fit multiple data sets (CSV and PDF in this example) into the \
          neccessary vector embeddings to be queried. Extensibly this data set could be sensitive \
              company information that a public model wouldn't have access to. For the model we are using \
                  OPEN-AIs GPT 3.5-Turbo. Costs are resonable; typically it only costs a few cents per query.")


st.subheader('app.py')
st.code(
"""
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

messages = st.session_state.get("messages", [])
for message in messages:
    if isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
"""
)


st.subheader('main.py')
st.code(
"""
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from pdf import porsche_engine
import streamlit as st


def complete_llm(input_prompt):
    stat_sheet_path = os.path.join("data", "porsche_911.csv")
    stat_sheet_df = pd.read_csv(stat_sheet_path)


    prices_query_engine = PandasQueryEngine(df=stat_sheet_df, verbose=False, instruction_str=instruction_str)
    prices_query_engine.update_prompts({"pandas_prompt":new_prompt})


    tools = [
        note_engine,
        QueryEngineTool(
            query_engine=prices_query_engine, 
            metadata=ToolMetadata(
                name="Porsche_stat_sheet",
                description="this give information about porsche specs over many years"
            ),
        ),
        QueryEngineTool(
            query_engine=porsche_engine, 
            metadata=ToolMetadata(
                name="Porsche_wiki",
                description="this give information about Porsches via Wikipedia"
            ),
        ),
    ]

    llm = OpenAI(model="gpt-3.5-turbo-0613")
    agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

    if input_prompt != None:
        response = agent.query(input_prompt)
        response = agent.chat(input_prompt)
        return response
    
"""
)


