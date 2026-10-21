import os
import pymysql
from sqlalchemy.engine import make_url
from main_jkb_with_country import app
from model import db

SEED_FILE = os.environ.get("SEED_FILE", "/app/demo/seed_demo_data.sql")


def load_seed():
    url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    conn = pymysql.connect(host=url.host, port=url.port or 3306, user=url.username,
                           password=url.password, database=url.database, autocommit=True)
    with open(SEED_FILE, encoding="utf-8") as f:
        statements = [s.strip() for s in f.read().split(";\n") if s.strip()]
    with conn.cursor() as cur:
        for stmt in statements:
            cur.execute(stmt)
    conn.close()
    print(f"Seed loaded: {len(statements)} statements")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created.")
    if os.environ.get("SEED_DEMO_DATA", "false").lower() == "true":
        load_seed()
