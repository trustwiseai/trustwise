from pydantic import BaseModel
from typing import List, Optional


class Chunk(BaseModel):  # Pydantic Model for Retrieved Nodes
    retrieved_node_text: str
    retrieved_node_score: float
    retrieved_node_id: str


class UploadData(BaseModel):  # Pydantic Model for data uploaded to the Evaluation endpoint
    user_id: int
    experiment_id: str
    query: str
    context: List[Chunk]
    response: str
    context_aggregated: str  # Context as a single string


class LoggingPayload(BaseModel):  # Pydantic Model for Events Data to be logged to MongoDB
    user_id: int
    experiment_id: str
    trace_type: str
    event_type: str
    parent_id: Optional[str] = ""
    event_id: str
    event_time: str
    event_payload: str
