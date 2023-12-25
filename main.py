import chainlit as cl
from sql import sql_query_engine, sql_database
from llm import llm, embed_model, get_response_from_llm
from llama_index.callbacks import CallbackManager, LlamaDebugHandler

from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index import set_global_service_context, ServiceContext



# llama_debug = LlamaDebugHandler(print_trace_on_end=True)
# callback_manager = CallbackManager([llama_debug])
# service_context = ServiceContext.from_defaults(callback_manager=callback_manager, 
                                        #        llm=llm, embed_model=embed_model)

# Create a service context using the LLM and embed model
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

# Set the global service context to be used by all services
set_global_service_context(service_context)

# Define a list of query engine tools
# query_engine_tools = [
#     QueryEngineTool(
#         query_engine=sql_query_engine,
#         metadata=ToolMetadata(
#             name="Customer Loan Database",
#             description="Database containing the Loan Application Data table"
#         )
#     )
# ]

# # Create a subquery engine using the query engine tools, service context, and enabling asynchronous execution
# subquery_engine = SubQuestionQueryEngine.from_defaults(
#     query_engine_tools=query_engine_tools,
#     service_context=service_context,
#     use_async=True
# )

instructions = '''

(Correct Spelling Errors and Grammatical Errors)
IMP - Make sure to return unique/distinct results wherever required

Instructions:
    - For text datatype columns, utilize the "LIKE" clause with the "%" wildcard for filtering using where or having keyword.
    - Avoid using the "=" operator for filtering in case of text datatype columns.
    - In case information exists across `books_data` and `books_rating` table then join them using the `title` column
    - When using joins, make sure you are using table name or alias with all column names to avoid ambiguity
    - For author or authors name, use `authors` column of `books_data` table

Please check for and correct any potential spelling mistakes in the conditions.
'''
# - For books related info, refer to `books_data` table and for reviews refer `books_rating` table. Please use the schema details to understand which table is required.
# Define a message handler function using the ChatLayer decorator

@cl.on_message
async def main(message: cl.Message):
    # Process the message content using the subquery engine
    sql_query = str(sql_query_engine.query(message.content+instructions)).replace('sql','').strip().replace('\n', ' ')
    print(sql_query)
    sql_result = sql_database.run_sql(sql_query)
    response = get_response_from_llm(message.content, sql_query, sql_result)

    additional_element = [
        cl.Text(name="SQL Query", content=sql_query, display="inline", language="sql")
    ]

    # Send the response to end-user
    await cl.Message(content=str(response), elements=additional_element).send()