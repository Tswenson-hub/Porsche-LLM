import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from pdf import porsche_engine

stat_sheet_path = os.path.join("data", "porsche_911.csv")
stat_sheet_df = pd.read_csv(stat_sheet_path)


prices_query_engine = PandasQueryEngine(df=stat_sheet_df, verbose=True, instruction_str=instruction_str)
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

while (prompt := input("Enter a prompt (q to quit)")) != "q":
    result = agent.query(prompt)
    print(result)