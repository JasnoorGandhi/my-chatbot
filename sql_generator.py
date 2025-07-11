from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import sqlparse
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# System prompt for generating SQL queries
sql_prompt_template = """
You are an expert SQL query generator for PostgreSQL. Based on the provided database schema and user question, generate a syntactically correct SQL query. 

IMPORTANT RULES:
1. Use only the column names and table names provided in the schema
2. Do not query columns that do not exist
3. Qualify column names with table names when needed
4. For student-related queries, use the 'students' table with these columns:
   - student_id, full_name, email, phone, enrollment_date, batch_id, status, total_fee, fee_paid, last_payment_date, remarks
   - status can be 'active', 'completed', or 'dropped'
   - batch_id values are typically 101, 102, 103, etc.
5. For trainer-related queries, use the 'trainers' table
6. For batch-related queries, use the 'trainer_batches' table
7. For interview-related queries, use the 'interviews' table
8. For array columns (like days TEXT[]), use 'ANY' or '@>' for comparisons. Example: WHERE 'Monday' = ANY(days)
9. Keep queries simple - avoid unnecessary JOINs unless specifically needed
10. Return only the SQL query without additional explanation or code fences

Schema: {schema}
Question: {question}
SQL Query:
"""

sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=sql_prompt_template
)

# SQL query generation chain
sql_chain = (
    {"schema": lambda x: x["schema"], "question": lambda x: x["question"]}
    | sql_prompt
    | llm
    | StrOutputParser()
)

# Function to generate SQL query
def generate_sql_query(schema, question):
    return sql_chain.invoke({"schema": schema, "question": question})

# Function to validate and parse SQL query
def parse_sql_query(query, engine):
    try:
        # Parse SQL query using sqlparse
        parsed = sqlparse.parse(query)
        if not parsed or len(parsed) != 1:
            return "Invalid SQL: Multiple statements or empty query", False
        
        # Validate syntax by attempting to format
        formatted_query = sqlparse.format(query, reindent=True)
        
        # Validate with PostgreSQL connection using text()
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text(f"EXPLAIN {query}"))
        return formatted_query, True
    except Exception as e:
        return str(e), False

# Function to execute SQL query
def execute_sql_query(query, engine):
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text(query))
            # Get column names from result keys
            columns = result.keys()
            rows = result.fetchall()
            return {"columns": list(columns), "rows": rows}, True
    except Exception as e:
        return str(e), False

def summarize_results(question, columns, rows):
    # Convert rows to a readable string
    if not rows:
        return "No results found."
    data_str = ""
    for row in rows:
        row_str = ", ".join([f"{col}: {val}" for col, val in zip(columns, row)])
        data_str += row_str + "\n"
    # Prompt for the LLM
    summary_prompt = f"""
You are an assistant. Given the following question and SQL query results, provide a concise, human-readable answer in natural language.

Question: {question}
Results:
{data_str}

Answer:
"""
    return llm.invoke(summary_prompt)