# 🦉 Trustwise Safety Module

The Trustwise Safety Module is a Python package designed to evaluate the RAG pipelines of a Language Model (LLM). It provides an aggregated Safety Score, along with various other individual scores and logs events during the query and index construction of the pipelines. Users can conveniently check event logs and safety score results stored in a MongoDB backend.

## 🔧 Installation

Install the Trustwise Safety Module using pip:

```python
pip install trustwise
```

## 🔥 Features

1. Evaluate RAG pipelines of an LLM.
2. Aggregated Safety Score calculation.
3. Event logging during query and index construction.
4. Backend storage in MongoDB.
5. Support for bulk scanning of responses from LLMs.

## 🚀 Usage with Llama Index

```python

from llama_index.callbacks import CallbackManager
from trustwise.callback import TrustwiseCallbackHandler
from trustwise.request import request_eval

# Initialise Trustwise Callback Handler
tw_callback = TrustwiseCallbackHandler()

# Configure the Handler with LlamaIndex Callback Manager
callback_manager = CallbackManager([tw_callback])

# Enter Trustwise API Key
tw_api_key = 'TRUSTWISE_API_KEY'

# Set the API key using the set_api_key method
tw_callback.set_api_key(tw_api_key)

# Initialise Experiment ID for tracking scans and events
experiment_id = tw_callback.set_experiment_id()

# Rest of the llamaindex code like indexing, llm response generation comes here

###### Evaluate LLM responses #######

scores = request_eval(api_key=tw_api_key,experiment_id=experiment_id, query=query, response=response)
print(scores)
```
### 🔐 Trustwise API Key
Get your API Key by logging in through Github -> [link](http://35.199.62.235/:8080/github-login)

## Contributing
We welcome contributions! If you find a bug, have a feature request, or want to contribute code, please create an issue or submit a pull request.

## 🪪 License
This project is licensed under the MIT License - see the LICENSE file for details.
