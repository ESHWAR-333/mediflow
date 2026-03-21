from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
import uuid

class Event(BaseModel):
    event_id: str
    event_type: str
    schema_version: str = "1.0"
    source: str
    timestamp: datetime
    data: Dict[str, Any]

    @staticmethod
    def create(event_type: str, source: str, data: Dict[str, Any]):
        return Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=source,
            timestamp=datetime.utcnow(),
            data=data
        )