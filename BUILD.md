# Steps to create and upload pip package for Trustwise
## Prepare your setup.py file

## Install setuptools
```sh
pip install setuptools wheel
```

## Create distribution
```sh
python setup.py sdist bdist_wheel
```

## Install `twine` for uploading package

```sh
pip install twine
```

## Upload your package to `pypi`
```sh
python -m twine upload dist/*
```

# Check installation of Trustwise package

## Create and activate virtual env 

```sh
python -m venv venv

source venv/bin/activate
```

## Install the package

```sh
pip install trustwise
```

## Test the imports in a Jupyter notebook

```python

from trustwise.callback import TrustwiseCallbackHandler
from trustwise.request import request_eval

```
If the above imports work fine, then you have successfully installed `trustwise`.
