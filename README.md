# Trustwise Safety Module

The Trustwise Safety Module is a Python package designed to evaluate the RAG pipelines of a Language Model (LLM). It provides an aggregated Safety Score, along with various other individual scores and logs events during the query and index construction of the pipelines. Users can conveniently check event logs and safety score results stored in a MongoDB backend.

## Installation

Install the Safety Module using pip:

```python
pip install safety
```

## Features

1. Evaluate RAG pipelines of an LLM.
2. Aggregated Safety Score calculation.
3. Event logging during query and index construction.
4. Backend storage in MongoDB.
5. Support for bulk scanning of responses from LLMs.

## Usage with Llama Index

```python

from trustwise.callback import TWCallbackHandler
from llama_index.callbacks import CallbackManager, LlamaDebugHandler

# Initialize Trustwise CallbackHandler
tw_callback = TWCallbackHandler()

# Enter Trustwise API Key
tw_api_key = 'TRUSTWISE_API_KEY'

# Set the API key using the set_api_key method
tw_callback.set_api_key(tw_api_key)

# Initialize LlamaDebugHandler object
llama_debug = LlamaDebugHandler(print_trace_on_end=True)

# Include Trustwise CallbackHandler in the LlamaIndex callback manager
tw_callback_manager = CallbackManager([llama_debug, tw_callback])

# Rest of the llamaindex code like indexing, llm response generation comes here

###### Evaluate LLM responses #######

from trustwise.functions import Observability

observe = Observability()

observe.set_api_key(tw_api_key)

results = observe.evaluate(query, response)
```
### Trustwise API Key
Get your API Key -> 

## Contributing
We welcome contributions! If you find a bug, have a feature request, or want to contribute code, please create an issue or submit a pull request.


