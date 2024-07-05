import string
import json


def validate_and_correct_response(response_text):
    try:
        # Attempt to parse the JSON
        response = json.loads(response_text)
        if "answer" in response and "explanation" in response:
            return response
        
        else:
            raise ValueError("Missing required fields")
        
    except (json.JSONDecodeError, ValueError):
        # If parsing fails, attempt to correct common issues

        response_text = response_text.strip()

        if response_text.startswith("{") and not response_text.endswith("}"):
            response_text += "}"

        if response_text.endswith("}") and not response_text.startswith("{"):
            response_text = "{" + response_text

        try:
            # Attempt to parse the JSON
            response = json.loads(response_text)
            if "answer" in response and "explanation" in response:
                
                return response
            else:
                
                raise ValueError("Missing required fields")
            
        except (json.JSONDecodeError, ValueError):
            # If it still fails, return a default error response
            
            return {"answer": "", "explanation": "Error: Invalid response format"}


def query_model(model, test_instrument_filename, client, base_prompt):
    """
    Query function for a specific model and test instrument.
    Returns model responses and overall score
    """

    with open(test_instrument_filename, "r") as file:
        test_instrument = json.load(file)

    # Query model

    model_responses = []
    for item in test_instrument:
        question = item["question"]
        choices = " ".join([f"({letter}) {choice}" for letter, choice in zip(
            string.ascii_lowercase, item["choices"])])
        prompt = f"{base_prompt}\nPregunta: {question}\nOpciones: {choices}"

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
        )
        r = chat_completion.choices[0].message.content
        model_responses.append(r)

    # for response in model_responses:
    #     try:
    #         json_res = json.loads(response)
    #         # print("SUCCESS")
    #         # print(response)
    #         # print(json_res["answer"])
    #         # print(json_res["explanation"])
    #         # print()

    #     except Exception:
    #         print("FAILURE")
    #         print(response)
    #         print()

    json_model_responses = [validate_and_correct_response(response)
                            for response in model_responses]

    # Compute score

    correct_answers = [item["answer"] for item in test_instrument]
    model_answers = [response["answer"] for response in json_model_responses]
    score = sum(1 for i in range(len(correct_answers))
                if model_answers[i] == correct_answers[i])
    score_percentage = score / len(correct_answers)

    return json_model_responses, score_percentage
