from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database connection
# Use DATABASE_URL for Render deployment, fallback to local for development
db_uri = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:secretpassword@localhost:5432/mydb")

# Handle Render's DATABASE_URL format (they sometimes add ?sslmode=require)
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

db = SQLDatabase.from_uri(db_uri)
engine = create_engine(db_uri)

def get_db():
    return db

def get_engine():
    return engine

def initialize_database():
    """Initialize database with schema and sample data if tables don't exist"""
    try:
        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            existing_tables = [row[0] for row in result]
            
            if not existing_tables:  # Database is empty
                print("Initializing database with schema and sample data...")
                # Read and execute setup_db.sql
                with open('setup_db.sql', 'r') as f:
                    sql_script = f.read()
                
                # Split the script into individual statements
                statements = sql_script.split(';')
                for statement in statements:
                    statement = statement.strip()
                    if statement:  # Skip empty statements
                        conn.execute(text(statement))
                
                conn.commit()
                print("Database initialized successfully!")
            else:
                print("Database already has tables, skipping initialization.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Don't raise the error - let the app continue