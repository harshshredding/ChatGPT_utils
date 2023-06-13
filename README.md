# ChatGPT_utils
Some useful code for querying ChatGPT. 


## Requirements
Works with `Python version 3.10` and above ; We use an [Anaconda](https://www.anaconda.com/download) python 3.10 environment.

You can create an anaconda python 3.10 environment called `my_env` with:
```bash
conda create --name my_env python=3.10
```

To install dependencies, do the following in your environment:
```bash
pip install -r requirements.txt
```

## Usage
Run `python chatgpt.py` to query chatgpt twice with the following two queries:  
```
1) What is the capital of France ?
2) What is the capital of India ?
```
It should return store the following results in the file `./test.json`:
```
[[0, "The capital of France is Paris."], [1, "The capital of India is New Delhi."]]
```
