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

## Upload your package to `testpypi`
```sh
python -m twine upload --repository testpypi dist/*
```

# Check installation of Trustwise package

## Create and activate virtual env 

```sh
python -m venv venv

source venv/bin/activate
```

## Install the package

```sh
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple tw-hop==1.0.1
```

## Test the imports in a Jupyter notebook

```python

from tw_hop.callback import TWCallbackHandler
from tw_hop import functions

```
If the above imports work fine, then you have successfully installed `tw-hop`.
