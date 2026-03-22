from app.consumer import start_consumer
from app.models import Base
from app.db import engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    start_consumer()