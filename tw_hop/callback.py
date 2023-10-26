import uuid
import requests
from tw_hop import config
import logging
import pymongo
import pandas as pd
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from llama_index.callbacks.base_handler import BaseCallbackHandler
from llama_index.callbacks.schema import CBEvent, CBEventType, EventPayload


def _generate_random_id() -> str:
    """Generates a random ID.

    Returns:
        str: A random ID.
    """
    return str(uuid.uuid4())


def handle_query(event):
    if event.event_type == CBEventType.QUERY:
        load = event.payload[EventPayload.QUERY_STR]
    return load


def handle_retrieve(event):
    if event.event_type == CBEventType.RETRIEVE:
        node_datas = []
        for node_with_score in event.payload[EventPayload.NODES]:
            node = node_with_score.node
            score = node_with_score.score

            node_data = {
                "id": node.hash,
                "node_text": node.text,
                "node_score": score
            }

            node_datas.append(node_data)
    return node_datas


def handle_llm(event):
    if event.event_type is CBEventType.LLM:
        response_text = str(event.payload[EventPayload.RESPONSE]) or str(event.payload[EventPayload.COMPLETION])
    return response_text


def validate_api_key(api_key):
    base_validate_url = config.base_validate_url
    headers = {'accept': 'application/json'}
    params = {'api_key': api_key}
    try:
        response = requests.post(base_validate_url, headers=headers, params=params)

        if response.status_code == 200:
            user_id = response.json()
            return user_id
        else:
            logging.error("API Key is invalid!, Please visit -> http://54.144.17.111:8000/github-login")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed with an exception: {str(e)}")
        return None


class TWCallbackHandler(BaseCallbackHandler):

    def __init__(self, callback: Optional[Callable] = None, api_key: Optional[str] = None) -> None:
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])
        self._callback = callback
        self._trace_data = pd.DataFrame()
        self._event_pairs = []
        self._user_id = validate_api_key(api_key)

    def set_api_key(self, api_key: str):
        if api_key is not None:
            self._user_id = validate_api_key(api_key)
            print("API Key is Authenticated!")
        else:
            logging.error("API Key is invalid!, Please visit -> http://54.144.17.111:8000/github-login")
            raise ValueError("API Key is invalid!")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        self._event_pairs = []
        if trace_id == "query":
            self._trace_data['Time Stamp'] = datetime.now().isoformat()
            self._trace_data['ID'] = _generate_random_id()

        if trace_id == "index_construction":
            self._trace_data['Time Stamp'] = datetime.now().isoformat()
            self._trace_data['ID'] = _generate_random_id()

    def end_trace(
            self,
            trace_id: Optional[str] = None,
            trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        if trace_id == "query":
            payload = {
                "trace_type": trace_id,
                "events": self._event_pairs,
                "user_id": self._user_id
            }

            response = requests.post(url=config.mongodb_logging_url, json=payload)
            
            if response.status_code == 200:
                response_json = response.json()
                logging.info(msg=response_json['message'])
            
            '''
            for event in self._event_pairs:
                mongo_url = "mongodb+srv://nihal:Pixel@sys-record.idbjhbn.mongodb.net/"  # TODO make an API call
                client = pymongo.MongoClient(mongo_url)
                db = client["system-record-test"]
                collection = db["log-testing"]
                data = {'user_id': self._user_id,
                        'event': event}
                insert_result = collection.insert_one(data)
                if insert_result.acknowledged:
                    logging.info(msg="Query events logged to Database")
            '''
        if trace_id == "index_construction":
            if self._user_id is None:
                raise Exception("User ID Problems")
            
            payload = {
                "trace_type": trace_id,
                "events": self._event_pairs,
                "user_id": self._user_id
            }

            response = requests.post(url=config.mongodb_logging_url, json=payload)
            
            if response.status_code == 200:
                response_json = response.json()
                logging.info(msg=response_json['message'])
            

            '''
            for event in self._event_pairs:
                mongo_url = "mongodb+srv://nihal:Pixel@sys-record.idbjhbn.mongodb.net/"  # TODO make an API call
                client = pymongo.MongoClient(mongo_url)
                db = client["system-record-test"]
                collection = db["index-log-testing"]
                data = {'user_id': self._user_id,
                        'event': event}
                insert_result = collection.insert_one(data)
                if insert_result.acknowledged:
                    logging.info(msg="Index events logged to Database")
            '''
    def on_event_start(
            self,
            event_type: CBEventType,
            payload: Optional[Dict[str, Any]] = None,
            event_id: str = "",
            parent_id: str = "",
            **kwargs: Any,
    ) -> None:

        if payload is not None:
            event = CBEvent(event_type, payload=payload, id_=event_id)

            if event.event_type == CBEventType.QUERY:
                load = handle_query(event)

            elif event.event_type == CBEventType.CHUNKING:
                load = payload[EventPayload.CHUNKS]

            else:
                load = str(event.payload)

            self._event_pairs.append(
                {
                    "event_type": str(event.event_type.name),
                    "event_id": str(event.id_),
                    "event_payload": load,
                    "event_time": str(event.time)
                })

    def on_event_end(
            self,
            event_type: CBEventType,
            payload: Optional[Dict[str, Any]] = None,
            event_id: str = "",
            **kwargs: Any,
    ) -> None:
        if payload is None:
            return

        if payload is not None:
            event = CBEvent(event_type, payload=payload, id_=event_id)
            if event.event_type == CBEventType.RETRIEVE:
                load = handle_retrieve(event)

            elif event.event_type == CBEventType.LLM:
                load = handle_llm(event)

            else:
                load = str(event.payload)

            self._event_pairs.append(
                {
                    "event_type": str(event.event_type.name),
                    "event_id": str(event.id_),
                    "event_payload": load,
                    "event_time": str(event.time)
                })
