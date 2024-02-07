import os
import requests
import logging
from dotenv import load_dotenv

# Load Environment
load_dotenv()

logging.basicConfig()  # Add logging level here if you plan on using logging.info() instead of my_logger as below.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO remove this as this has been moved into the backend
def validate_api_key(api_key):
    base_validate_url = os.getenv('validate_key_url')
    headers = {'accept': 'application/json'}
    params = {'api_key': api_key}
    try:
        response = requests.post(base_validate_url, headers=headers, params=params)

        if response.status_code == 200:
            user_id = response.json()
            return user_id
        else:
            logger.error(f"API Key is invalid!, Please visit -> http://35.199.62.235:8080/github-login")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed with an exception: {str(e)}")
        return None
