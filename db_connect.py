from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database connection
db_uri = os.getenv("DATABASE_URI", "postgresql+psycopg2://postgres:secretpassword@localhost:5432/mydb")
db = SQLDatabase.from_uri(db_uri)
engine = create_engine(db_uri)

def get_db():
    return db

def get_engine():
    return engine