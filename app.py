import streamlit as st
from langchain_community.llms import Ollama
import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain_experimental.sql import SQLDatabaseChain
from sqlalchemy import create_engine
from langchain_groq import ChatGroq

groq_api_key = "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"

# Step 1: Initialize LangChain's LLM (Ollama)
llm = ChatGroq(groq_api_key=groq_api_key,
               model_name="llama3-groq-70b-8192-tool-use-preview")  # Replace with your specific Ollama model name

# Step 2: Set up SQLAlchemy connection to MySQL database
engine = create_engine("mysql+mysqldb://root:Fruitloop7$@localhost/training")
db = SQLDatabase(engine)

# Step 3: Define a Tool for querying the database
def query_database(query: str):
    sql_chain = SQLDatabaseChain.from_llm(llm, db)
    return sql_chain.run(query)

sql_tool = Tool(
    name="Query SQL Database",
    func=query_database,
    description="Executes SQL queries and retrieves data from the MySQL database."
)

# Step 4: Set up an Agent to use the tool
tools = [sql_tool]
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", handle_parsing_errors=True, verbose=True)

# Step 5: Streamlit App Layout
st.title("SQL Query Interface")

# User input for the natural language query
user_input = st.text_input("Enter your query:")

# Define a prompt template
prompt_template = "Give a MYSQL query based on the following input: '{}'"


# Button to submit the query
if st.button("Submit"):
    # Create a prompt using the user input
    prompt = prompt_template.format(user_input)
    
    # Process the prompt to generate the SQL query
    with st.spinner("Generating SQL query..."):
        try:
            generated_query = agent.run(prompt)
            # Display the generated SQL query
            st.subheader("Generated SQL Query:")
            st.write(generated_query)
            print("Generated Query: ", generated_query)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.subheader("Debug Information:")
            st.write(f"Prompt: {prompt}")

# Optional: Add a clear button to reset the input field
if st.button("Clear"):
    st.experimental_user()  # This clears the input by re-running the app
