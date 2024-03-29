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

user_id = "Enter your User ID"
scan_name = "Enter your Scan Name"

tw_callback = TrustwiseCallbackHandler(user_id=user_id, scan_name=scan_name)

# Configure the Handler with LlamaIndex Callback Manager
callback_manager = CallbackManager([tw_callback])

# Rest of the llamaindex code like indexing, llm response generation comes here

###### Evaluate LLM responses #######

scores = request_eval(user_id=user_id,scan_name=scan_name, query=query, response=response)
print(scores)
```
### 🔐 Trustwise API Key
Get your API Key by logging in through Github -> [link](http://35.199.62.235:8080/github-login)

## Contributing
We welcome contributions! If you find a bug, have a feature request, or want to contribute code, please create an issue or submit a pull request.

## 🪪 License
This project is licensed under the MIT License - see the LICENSE file for details.
