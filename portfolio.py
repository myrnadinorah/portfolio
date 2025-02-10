
import os
from sqlalchemy import create_engine

mysql_connection_string = os.getenv("MYSQL_CONNECTION_STRING")

if not mysql_connection_string:
    raise ValueError("❌ MYSQL_CONNECTION_STRING is missing from the environment variables!")

print(f"🔍 Debug: {mysql_connection_string}")  # Ensure password is correct

# Attempt database connection
try:
    engine = create_engine(mysql_connection_string)
    conn = engine.connect()
    print("✅ Successful SQLAlchemy connection!")
    conn.close()
except Exception as e:
    print(f"❌ SQLAlchemy Error: {e}")
