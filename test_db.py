from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DB_URI"))
with engine.connect() as conn:
    print(conn.execute(text("SELECT 1")).fetchall())