import os
import yaml
from dotenv import load_dotenv
from itertools import product
import json
from groq import Groq

from model import query_model


load_dotenv()

with open("config.yaml", "r") as file:
    params = yaml.safe_load(file)

base_prompt = params["base_prompt"]
models = params["models"]
test_instruments = params["test_instruments"]
iters = params["iters"]
id = params["id"]


# Groq client

api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError(
        "API key not found. Please set the GROQ_API_KEY in the .env file."
    )

client = Groq(
    api_key=api_key,
)

# Inference

results = {}

for i in range(1, iters + 1):
    for model, test_instrument in product(models, test_instruments):
        test_instrument_name = test_instrument['name']
        test_instrument_filename = test_instrument['filename']
        print(f"Modelo: {model}")
        print(f"Instrumento: {test_instrument_name}")
        print()
        responses, score = query_model(model,
                                    test_instrument_filename, 
                                    client, 
                                    base_prompt)

        if model not in results:
            results[model] = {}

        results[model][test_instrument_name] = {
            "responses": responses,
            "score": score
        }

        # Save results to JSON file

        os.makedirs("results", exist_ok=True)
        file_id = iters * id + i
        with open(f"results/results_{model}_{test_instrument_name}_{file_id}.json", "w") as file:
            json.dump(results, file)
            results = {}
