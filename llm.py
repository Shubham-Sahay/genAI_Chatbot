import os
import sys

from llama_index.llms import Gemini
from llama_index.embeddings import GooglePaLMEmbedding

from dotenv import load_dotenv
load_dotenv()

import nest_asyncio
nest_asyncio.apply()

import warnings
warnings.filterwarnings('ignore')

# Initializing Google Gemini LLM model as the LLM 
llm = Gemini()

# Initializing Google gecko embedding
model_name = "models/embedding-gecko-001"
embed_model = GooglePaLMEmbedding(model_name=model_name)

def get_response_from_llm(user_query, sql_query, sql_response, llm=llm):

    prompt = f"""User Query: {user_query}
                 SQL Query: {sql_query}
                 SQL Response: {sql_response}
                 
                 Using the query and response, write a natural languge response to the user query. 
                 
                 Please make sure not to make up answers. If you don't know, just say you don't know.
                 """

    llm_response = llm.complete(prompt)
    
    return llm_response

