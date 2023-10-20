import requests
import json
import uuid
import config
import pandas as pd


def validate_api_key(api_key):
    base_validate_url = config.base_validate_url
    headers = {'accept': 'application/json'}
    params = {'api_key': api_key}
    response = requests.post(base_validate_url, headers=headers, params=params)
    user_id = response.json()
    return user_id


class Observability:

    # TODO add a docstring for this function
    def set_api_key(self, api_key: str):
        if api_key is not None:
            self._user_id = validate_api_key(api_key)
            print("User Authenticated!")
        else:
            raise ValueError("API Key is invalid!")

    # TODO add a docstring for this function
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

        dat = res.json()
        df = pd.DataFrame(dat)
        print("")
        print("Results:")
        return df
