from app.db import init_db
from app.consumer import start_consumer

if __name__ == "__main__":
    init_db()
    start_consumer()