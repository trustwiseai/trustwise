import os
import requests
import logging
from dotenv import load_dotenv

# Load Environment
load_dotenv()


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
            logging.error(f"API Key is invalid!, Please visit -> {os.getenv('github_login_url')}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed with an exception: {str(e)}")
        return None
