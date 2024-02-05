import os
import requests
import logging
from ratelimit import limits, sleep_and_retry
from trustwise.dtos.models import Chunk, UploadData
from trustwise.utils import validate_api_key

logging.basicConfig()  # Add logging level here if you plan on using logging.info() instead of my_logger as below.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Define the rate limit (e.g., 3 requests per 30 seconds)
@sleep_and_retry
@limits(calls=3, period=30)
def send_request(url, data_dict):
    response_object = requests.post(url, json=data_dict)
    return response_object


def request_eval(api_key, experiment_id, query, response):

    if api_key is not None:
        user_id = validate_api_key(api_key)
        print(f"API Key is Authenticated! - User ID : {user_id}")
        pass
    else:
        logging.error(f"API Key is invalid!, Please visit -> {os.getenv('github_login_url')}")
        raise ValueError("API Key is invalid!")

    # Evaluation URL
    eval_url = os.getenv('evaluation_url')

    context_aggregated = ''  # Context retrieved from the RAG pipeline to be stored as a string for evaluations
    context = []  # Context chunks to be logged in the record with text, score and node id.

    for node in response.source_nodes:
        context_aggregated += node.text
        node_text = node.text
        node_score = node.score
        node_id = node.id_

        chunk = Chunk(retrieved_node_text=node_text, retrieved_node_score=node_score, retrieved_node_id=node_id)
        context.append(chunk)

    # Data to be uploaded to the endpoint for the evaluations to run
    data = UploadData(user_id=user_id, experiment_id=experiment_id, query=query, context=context,
                      response=response.response, context_aggregated=context_aggregated)

    try:
        data_dict = data.model_dump()  # Convert to dict for JSON serialization
        response_object = send_request(url=eval_url, json=data_dict)
        response_object.raise_for_status()  # Check for HTTP errors

        # Check if the response has a valid JSON content type
        if 'application/json' in response_object.headers.get('Content-Type', ''):
            return response_object.json()
        else:
            logger.error(f"Unexpected response content type: {response_object.headers.get('Content-Type', '')}")
            return None  # Handle the case where the response is not JSON

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during request: {e}")
        return None  # Handle request exceptions
