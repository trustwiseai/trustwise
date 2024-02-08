import requests
import logging
from trustwise.models import Chunk, UploadData
from trustwise.config import TW_EVALUATION_URL


logging.basicConfig()  # Add logging level here if you plan on using logging.info() instead of my_logger as below.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def request_eval(user_id, experiment_id, query, response, api_key=None):

    # context_aggregated = ''  # Context retrieved from the RAG pipeline to be stored as a string for evaluations
    context = []  # Context chunks to be logged in the record with text, score and node id.

    for node in response.source_nodes:
        # context_aggregated += node.text
        node_text = node.text
        node_score = node.score
        node_id = node.id_

        chunk = Chunk(node_text=node_text, node_score=node_score, node_id=node_id)
        context.append(chunk)

    # Data to be uploaded to the endpoint for the evaluations to run
    data = UploadData(user_id=user_id, experiment_id=experiment_id, query=query, context=context,
                      response=response.response, api_key=api_key)

    try:
        data_dict = data.model_dump()  # Convert to dict for JSON serialization
        response_object = requests.post(url=TW_EVALUATION_URL, json=data_dict)
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
