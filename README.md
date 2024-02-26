# Porsche-LLM
This RAG powered LLM makes use of "llama-index" modules to create two different query engines related to data about Porsche 911s. One piece of data is a flat CSV file that records mostly quantitative specs about a variety of different Porsches. Additionally, the Wikipedia page for Porsche 911 was downloaded as a PDF in full.

The underlying LLM is a gpt3.5 turbo which gives decent results particularly with the embedded, unstructured, PDF data. Questions intended for the engine powered by the CSV file require somewhat careful wording or the resulting Pandas query will return an error. However, simple counts, maxes, mins, and groupbys are relatively safe. 


