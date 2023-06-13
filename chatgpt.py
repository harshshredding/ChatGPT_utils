from typing import Callable
import time
from utils.general import show_progress, red, create_json_file_with_data, green
import os
import openai
from dotenv import load_dotenv, find_dotenv

# Configure openai client
_ = load_dotenv(find_dotenv()) # read local .env file with API key
openai.api_key = os.getenv('OPENAI_API_KEY') # grab our API key


def query_with_simple_template(query: str):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ]
    )
    return result.choices[0].message.content


def query_multiple(
        queries: list[str],
        output_file_path: str,
        query_with_template: Callable[[str],str]):
    """
    Query chatgpt with the given prompts sequentially and store the results
    in a file locally.

    Parameters:
        queries (list[str]): The queries for chatgpt. Usually, a query corresponds to a sample 
            in the dataset.
        output_file_path (str): The file we want to store ChatGPT's results in.
        query_with_template (function): A function that queries chatgpt using some prompting 
            template and returns ChatGPT's prediction.

    Examples:
        query_multiple(queries=['What is the capital of france ?', 'What is the capital of India'], output_file_path='./test.json', 
            query_with_template=query_with_simple_template)
    """
    chatgpt_completions = []

    for sample_idx, query in show_progress(enumerate(queries), total=len(queries)):
        time.sleep(1.5)
        chatgpt_prediction = 'ERROR'
        # If we fail try 2 more times
        for _ in range(3):
            try:
                chatgpt_prediction = query_with_template(query)
                # if successful, break and continue to next sample
                break
            except Exception as e:
                print(red("An error occurred."))
                print(e)
                print("waiting for 60 secs before trying again")
                time.sleep(60)
                print("Trying again")
        chatgpt_completions.append((sample_idx, chatgpt_prediction))
        if (sample_idx % 100) == 0:
            print("Storing intermediate results")
            create_json_file_with_data(output_file_path, chatgpt_completions)
    create_json_file_with_data(output_file_path, chatgpt_completions)
    print(green("Finished"))


def main():
    # An example:
    # We ask chatgpt for the capital of france and india, in two separate queries.
    query_multiple(
            queries=['What is the capital of france ?', 'What is the capital of India'], 
            output_file_path='./test.json', 
            query_with_template=query_with_simple_template)


if __name__ == '__main__':
    main()
