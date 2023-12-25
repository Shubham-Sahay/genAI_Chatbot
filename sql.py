import nest_asyncio
nest_asyncio.apply()

import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import warnings
warnings.filterwarnings('ignore')

from llama_index import VectorStoreIndex, ServiceContext, set_global_service_context, SQLDatabase
from llama_index.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from llama_index.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema
)

from llm import llm, embed_model

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select
    )

from sqlalchemy.engine import URL

import pandas as pd

from dotenv import load_dotenv
load_dotenv()


# Retrieve environment variables for SQL connection
server = os.getenv("SQL_SERVER_ADDRESS")
database = os.getenv("SQL_DATABASE")

print('Creating SQL Engine..')
# Create a SQLAlchemy engine to connect to the SQL Server database
# engine = create_engine(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
engine = create_engine(f'sqlite://{server}/{database}')

print('Creating Service Context..')
# Initialize the LLM and embed model (assumes these are already defined)
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

set_global_service_context(service_context)

# Create an instance of the SQLDatabase class using the SQLAlchemy engine
sql_database = SQLDatabase(engine=engine)
print('Sql database created...')

# Create an instance of the SQLTableNodeMapping class using the SQLDatabase object
table_node_mapping = SQLTableNodeMapping(sql_database)

# Define a list of SQLTableSchema objects, each representing a table in the database
table_schema_objs = [
    (SQLTableSchema(table_name="books_data",
                    context_str='''

The Books data table contains detailed information about 212,404 unique books it file is built by using
google books API to get details information about books it rated
Please refer to this table's column description of format `ColumnName`:`Description` to get the details of `books_data`. 
(Use only the defined column names to generate sql queries)
################
`Title`:`Book Title`
`Description`:`decription of book`
`authors`:`Name of book author or authors`
`image`:`url for book cover`
`previewLink`:`link to access this book on google Books`
`publisher`:`Name of the publisher`
`publishedDate`:`the date of publish`
`infoLink`:`link to get more information about the book on google books`
`categories`:`genres of books`
`ratingsCount`:`averaging rating for book`
################
''')),
    (SQLTableSchema(table_name="books_rating",
                    context_str='''

The Book Ratings table contain feedback about 500,000 user on 212404 unique books the data set is part of the Amazon review Dataset 
it contains product reviews and metadata from Amazon, including reviews spanning May 1996 - July 2014.
Please refer to this table's column description of format `ColumnName`:`Description` to get the details of `books_ratings`. 
(Use only the defined column names to generate sql queries)
################
`id`:`The Id of Book`
`Title`:`Book Title`
`Price`:`The price of Book`
`User_id`:`Id of the user who rates the book`
`profileName`:`Name of the user who rates the book`
`review_helpfulness`:`helpfulness rating of the review, e.g. 2/3`
`review_score`:`rating from 0 to 5 for the book`
`review_time`:`time of given the review`
`review_summary`:`the summary of a text review`
`review_text`:`the full text of a review`
################
'''))
]


# Create an instance of the ObjectIndex class using the table schema objects, table node mapping, and vector store index
obj_index = ObjectIndex.from_objects(table_schema_objs, table_node_mapping, VectorStoreIndex)
print('Object index created..')

# Create an instance of the SQLTableRetrieverQueryEngine class using the SQLDatabase object and object index
sql_query_engine = SQLTableRetrieverQueryEngine(sql_database, 
                                                obj_index.as_retriever(similarity_top_k=1),
                                                synthesize_response=False,
                                                sql_only=True
                                                )
                                                
print('Query Engine created..')

# print(sql_query_engine.query("How many records are in the table?"))