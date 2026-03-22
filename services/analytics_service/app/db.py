from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    with engine.connect() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                time        TIMESTAMPTZ       NOT NULL,
                event_id    TEXT              NOT NULL,
                event_type  TEXT              NOT NULL,
                source      TEXT              NOT NULL,
                booking_id  TEXT,
                patient_id  TEXT,
                doctor_id   TEXT,
                urgency_score INTEGER,
                payload     JSONB
            );
        """))

        try:
            conn.execute(text("""
                SELECT create_hypertable(
                    'analytics_events', 'time',
                    if_not_exists => TRUE
                );
            """))
            print("TimescaleDB hypertable ready: analytics_events")
        except Exception as e:
            print(f"Hypertable note: {e}")

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_analytics_event_type
            ON analytics_events (event_type, time DESC);
        """))

        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_analytics_booking_id
            ON analytics_events (booking_id, time DESC);
        """))

        conn.commit()
        print("Analytics DB initialized.")