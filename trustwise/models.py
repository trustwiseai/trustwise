from typing import List, Optional

from pydantic import BaseModel


class Chunk(BaseModel):  # Pydantic Model for Retrieved Nodes
    node_text: str
    node_score: float
    node_id: str


class UploadData(BaseModel):  # Pydantic Model for data uploaded to the Evaluation endpoint
    user_id: str
    scan_name: str
    scan_id: str
    project_id: Optional[str]
    query: str
    context: List[Chunk]
    response: str
    api_key: Optional[str]


class LoggingPayload(BaseModel):  # Pydantic Model for Events Data to be logged to MongoDB
    user_id: str
    scan_id: str
    project_id: str
    scan_name: str
    trace_type: str
    event_type: str
    parent_id: Optional[str] = ""
    event_id: str
    event_time: str
    event_payload: str
