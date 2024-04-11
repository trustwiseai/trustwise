from setuptools import setup, find_packages

setup(
    name="trustwise",
    version="3.1.4",
    description="Trustwise PyPi Package",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Trustwise",
    author_email="nihal@trustwise.ai",
    url="https://github.com/trustwiseai/trustwise",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        'llama-index~=0.9.36',
        'pydantic~=2.5.3',
        'requests~=2.31.0'
    ],)
