import streamlit as st
import sqlalchemy as sa
from langchain_groq import ChatGroq

# Set API key and database details
groq_api_key = "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"

# Set your MySQL server credentials
db_user = "root"
db_password = "Fruitloop7$"  # Update with your password
db_host = "localhost"

# Function to fetch metadata for all databases
def get_all_databases_metadata(engine):
    metadata_info = ""
    with engine.connect() as connection:
        # Fetch all database names
        databases = connection.execute(sa.text("SHOW DATABASES")).fetchall()

        for (database,) in databases:
            metadata_info += f"Database: {database}\n"
            # Connect to the database
            db_engine = sa.create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{database}")
            inspector = sa.inspect(db_engine)

            # Fetch tables and their columns
            for table_name in inspector.get_table_names():
                columns = inspector.get_columns(table_name)
                metadata_info += f"  Table: {table_name}\n"
                metadata_info += "    Columns:\n"
                for column in columns:
                    metadata_info += f"      - {column['name']} ({column['type']})\n"

    return metadata_info

# Set up the Streamlit app
st.title("Database Metadata App")
st.write("This app retrieves metadata for all databases in the MySQL server.")

# Initialize the MySQL server connection
try:
    engine = sa.create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}")
    st.success("Connected to the MySQL server successfully!")

    # Fetch and display database metadata
    metadata_info = get_all_databases_metadata(engine)
    st.write("Database Metadata:\n", metadata_info)

except Exception as e:
    st.error(f"Error connecting to the MySQL server: {e}")
    st.stop()

# Initialize the LLM (Ollama)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

# Define the query prompt
query_prompt = st.text_input("Enter your query:")
prompt_template = "Based on the following database schema:\n{}\nGenerate an appropriate MySQL query based on the input: '{}'"

# Generate SQL query and execute
if query_prompt:
    try:
        # Prepare the prompt
        prompt = prompt_template.format(metadata_info, query_prompt)
        st.write("Prompt:\n", prompt)

        # Generate the SQL query using the LLM without database exposure
        response = llm.invoke(prompt)  # Directly use the LLM with the prompt

        # Extract the query from the response
        query = response.strip()  # Assuming the response is just the query text
        st.write("Generated SQL Query:\n", query)

    except Exception as e:
        st.error(f"Error generating SQL query: {e}")
