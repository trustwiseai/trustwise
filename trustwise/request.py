import os
import utils
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


class UploadBulkData(BaseModel):  # Pydantic Model for bulk data uploaded to the Evaluation endpoint
    user_id: int
    experiment_id: str
    queries: List[str]
    context: List[str]
    responses: List[ResponseData]


def request_eval(api_key, experiment_id, query, response):

    if api_key is not None:
        user_id = utils.validate_api_key(api_key)
        print(f"API Key is Authenticated! - User ID : {user_id}")
        pass
    else:
        logging.error(f"API Key is invalid!, Please visit -> {os.getenv('github_login_url')}")
        raise ValueError("API Key is invalid!")

    url = os.getenv("evaluation_url")

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


def request_batch_eval(api_key, experiment_id, queries, responses, contexts):

    if api_key is not None:
        user_id = utils.validate_api_key(api_key)
        print(f"API Key is Authenticated! - User ID : {user_id}")
        pass
    else:
        logging.error(f"API Key is invalid!, Please visit -> {os.getenv('github_login_url')}")
        raise ValueError("API Key is invalid!")

    if len(queries) != len(responses) or len(queries) != len(contexts):
        raise ValueError("Input lists must have the same length.")

    # Data stored with respect to the response generated - Response string and context string for evaluations
    response_data_list = list(zip(responses, contexts))

    # Data to be uploaded to the endpoint for the evaluations to run
    data = UploadBulkData(user_id=user_id, experiment_id=experiment_id, queries=queries, contexts=contexts,
                          responses=response_data_list)

    url = "http://api.trustwise.ai/safety/v2/bulk_evaluation"

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
