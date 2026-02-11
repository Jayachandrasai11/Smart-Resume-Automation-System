import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def get_resume_db():
    try:
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            dbname="resume_db",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=int(os.getenv("POSTGRES_PORT", 5432))
        )
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")
