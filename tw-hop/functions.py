import requests
import json
import uuid
import config
import logging
import pandas as pd


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


class Observability:

    def __init__(self):
        self._user_id = None

    def set_api_key(self, api_key: str):
        if api_key is not None:
            self._user_id = validate_api_key(api_key)
            print("API Key is Authenticated!")
        else:
            logging.error("API Key is invalid!, Please visit -> http://54.144.17.111:8000/github-login")
            raise ValueError("API Key is invalid!")

    def evaluate(self, query, response):

        user_id = self._user_id

        data = {'user_id': user_id, "response": response.response, "source_nodes": []}

        cons = ''
        for node in response.source_nodes:
            cons = cons + node.text

        for node in response.source_nodes:
            data["source_nodes"].append({
                "node_id": node.id_,
                "text": node.text,
                "score": node.score
            })

        random_uuid = uuid.uuid4()
        scan_id = str(random_uuid)

        questions = [query]
        answers = [response.response]
        contexts = [cons]

        data_dict = {
            "query": questions,
            "response": answers,
            "context": contexts
        }

        data['scan_data'] = {
            "scan_id": scan_id,
            "scan_data": data_dict}

        url = config.evaluate_url

        json_data = json.dumps(data)
        headers = {'accept': 'application/json'}
        res = requests.post(url, headers=headers, data=json_data, json=None)

        if res.status_code == 200:
            dat = res.json()
            df = pd.DataFrame(dat)
            print("")
            print("Results:")
            return df

        else:
            logging.error(f"Evaluate request failed with status code {response.status_code}, Please try again later.")
            return None
