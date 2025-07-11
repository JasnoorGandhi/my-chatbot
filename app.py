import streamlit as st
from db_connect import get_db, get_engine
from schema_embed import extract_and_embed_schema, retrieve_relevant_schema, init_qdrant_collection
from sql_generator import generate_sql_query, parse_sql_query, execute_sql_query, summarize_results
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Streamlit app
st.set_page_config(page_title="AI SQL Query Assistant", layout="centered")
st.title("AI-Powered SQL Query Assistant")

# Initialize database and Qdrant
engine = get_engine()
init_qdrant_collection()
extract_and_embed_schema(engine)

# Streamlit UI
if st.button("Refresh Schema Embeddings"):
    from qdrant_client import QdrantClient
    qdrant_client = QdrantClient(url=os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))
    qdrant_client.delete_collection("schema_embeddings")
    init_qdrant_collection()
    extract_and_embed_schema(engine)
    st.success("Schema embeddings refreshed!")

if prompt := st.chat_input("Ask a question about the database:"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Step 1: Retrieve relevant schema
        relevant_schemas = retrieve_relevant_schema(prompt)
        schema_text = "\n".join(relevant_schemas)
        
        # Step 2: Generate SQL query
        sql_query = generate_sql_query(schema_text, prompt)
        st.write("Generated SQL Query:")
        st.code(sql_query, language="sql")
        
        # Step 3: Parse and validate SQL query
        parsed_query, is_valid = parse_sql_query(sql_query, engine)
        if not is_valid:
            st.error(f"SQL Query Error: {parsed_query}")
        else:
            # Step 4: Execute SQL query
            result, success = execute_sql_query(parsed_query, engine)
            if success:
                st.write("Query Results (Natural Language):")
                summary = summarize_results(prompt, result["columns"], result["rows"])
                if isinstance(summary, dict) and "content" in summary:
                    st.write(summary["content"])
                elif hasattr(summary, "content"):
                    st.write(summary.content)
                else:
                    st.write(str(summary))
            else:
                st.error(f"Execution Error: {result}")