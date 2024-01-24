import requests
import logging
from pydantic import BaseModel
from typing import List


class Chunk(BaseModel):  # Pydantic Model for Retrieved Nodes
    node_text: str
    node_score: float
    node_id: str


class ResponseData(BaseModel):  # Pydantic Model for Data related to Response generated
    response: str
    context: str


class UploadData(BaseModel):  # Pydantic Model for data uploaded to the Evaluation endpoint
    user_id: int
    experiment_id: str
    query: str
    context: List[Chunk]
    response: ResponseData


def validate_api_key(api_key):
    base_validate_url = "http://34.145.241.196:8080/validate_tw_key"
    headers = {'accept': 'application/json'}
    params = {'api_key': api_key}
    try:
        response = requests.post(base_validate_url, headers=headers, params=params)

        if response.status_code == 200:
            user_id = response.json()
            return user_id
        else:
            logging.error("API Key is invalid!, Please visit -> http://34.145.241.196:8080/github-login")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed with an exception: {str(e)}")
        return None


def request_eval(api_key, experiment_id, query, response):

    if api_key is not None:
        user_id = validate_api_key(api_key)
        print(f"API Key is Authenticated! - User ID : {user_id}")
        pass
    else:
        logging.error("API Key is invalid!, Please visit -> http://34.145.241.196:8080/github-login")
        raise ValueError("API Key is invalid!")

    url = "http://api.trustwise.ai/safety/v2/evaluation"

    cons = ''  # Context retrieved from the RAG pipeline to be stored as a string for evaluations
    context = []  # Context chunks to be logged in the record with text, score and node id.

    for node in response.source_nodes:
        cons += node.text
        node_text = node.text
        node_score = node.score
        node_id = node.id_

        chunk = Chunk(node_text=node_text, node_score=node_score, node_id=node_id)
        context.append(chunk)

    # Data stored with respect to the response generated - Response string and context string for evaluations
    response_data = ResponseData(response=response.response, context=cons)

    # Data to be uploaded to the endpoint for the evaluations to run
    data = UploadData(user_id=user_id, experiment_id=experiment_id, query=query, context=context, response=response_data)

    try:
        data_dict = data.model_dump()  # Convert to dict for JSON serialization
        response_object = requests.post(url, json=data_dict)
        response_object.raise_for_status()  # Check for HTTP errors

        # Check if the response has a valid JSON content type
        if 'application/json' in response_object.headers.get('Content-Type', ''):
            return response_object.json()
        else:
            print(f"Unexpected response content type: {response_object.headers.get('Content-Type', '')}")
            return None  # Handle the case where the response is not JSON

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None  # Handle request exceptions
