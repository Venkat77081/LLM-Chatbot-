import streamlit as st
from langchain_community.llms import Ollama
import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_groq import ChatGroq

# Set API key and database details
groq_api_key = "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"

db_user = "root"
db_password = "Fruitloop7$"
db_host = "localhost"
db_name = "training"

# Function to extract database schema
def get_database_schema(engine):
    schema_info = ""
    inspector = sa.inspect(engine)
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema_info += f"Table: {table_name}\n"
        for column in columns:
            schema_info += f"  - {column['name']} ({column['type']})\n"
    return schema_info

# Set up the Streamlit app
st.title("SQL Query App")
st.write("This app generates MySQL queries based on the input.")

# Initialize the database connection
try:
    engine = sa.create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    st.success("Connected to the database successfully!")
    
    # Get and display database schema
    schema_info = get_database_schema(engine)
    #st.write("Database Schema:\n", schema_info)

except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()

# Initialize the LLM (Ollama)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

# Create the SQL query chain
#generate_query = create_sql_query_chain(llm, db)

# Define the query prompt
query_prompt = st.text_input("Enter your query:")
prompt_template = "Based on the following database schema:\n{}\nGive an appropriate MYSQL query based on the input: '{}'"
#prompt = prompt_template.format(schema_info, query_prompt)
#st.write("promt :\n", prompt)

# # Generate SQL query and execute
# if query_prompt:
#     try:
#         prompt = prompt_template.format(schema_info, query_prompt)
#         #st.write("promt :\n", prompt)
#         #response = generate_query.invoke({"question": prompt})
#         response = llm.invoke(prompt)
#         #query = response.split("SQLQuery:")[-1].strip() if "SQLQuery:" in response else response.strip()
#         st.write(response)

#     except Exception as e:
#         st.error(f"Error executing query: {e}")

# Generate SQL query and execute
# Generate SQL query and execute
if query_prompt:
    try:
        prompt = prompt_template.format(schema_info, query_prompt)
        # Get the response from the LLM
        response = llm.invoke(prompt)

        # Access the content of the response
        response_content = response['content'] if isinstance(response, dict) else response.content

        # Extract the SQL query from the response content
        # Assuming the SQL query starts with "```sql" and ends with "```"
        start_idx = response_content.find("```sql") + len("```sql\n")
        end_idx = response_content.find("```", start_idx)
        sql_query = response_content[start_idx:end_idx].strip()  # Extracting and stripping the query

        # Display only the SQL query
        st.write("Generated SQL Query:")
        st.code(sql_query)

    except Exception as e:
        st.error(f"Error executing query: {e}")


