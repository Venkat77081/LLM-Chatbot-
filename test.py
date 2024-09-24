import streamlit as st
from langchain_community.llms import Ollama
import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_groq import ChatGroq
import os

# Set API key and database details
groq_api_key = "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"

db_user = "root"
db_password = "Fruitloop7$"
db_host = "localhost"
db_name = "training"

# Set up the Streamlit app
st.title("SQL Query App")
st.write("This app generates MySQL queries based on the input.")

# Initialize the database connection
try:
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    st.success("Connected to the database successfully!")
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()

# Initialize the LLM (Ollama)
llm = ChatGroq(groq_api_key=groq_api_key,
               model_name="gemma2-9b-it")

# Create the SQL query chain
generate_query = create_sql_query_chain(llm, db)

# Define the query prompt
query_prompt = st.text_input("Enter your query:")
prompt_template = "Give a appropriate MYSQL query based on the input and the database: '{}'"
prompt = prompt_template.format(query_prompt)

# Generate SQL query and execute
if query_prompt:
    try:
        response = generate_query.invoke({"question": prompt})
        query = response.split("SQLQuery:")[-1].strip() if "SQLQuery:" in response else response.strip()
        print(query)
        #st.write("Generated SQL Query:", query)
        st.write(query)        

    except Exception as e:
        st.error(f"Error executing query: {e}")
