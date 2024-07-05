import string
import json


def query_model(model, test_instrument_filename, client, base_prompt):
    """
    Query function for a specific model and test instrument.
    Returns model responses and overall score
    """

    with open(test_instrument_filename, "r") as file:
        test_instrument = json.load(file)

    # Query model

    model_response = []
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
        r = chat_completion.choices[0].message.content.strip()
        model_response.append(r)

    # Compute score

    correct_answers = [item["answer"] for item in test_instrument]
    score = sum(1 for i in range(len(correct_answers)) if model_response[i] == correct_answers[i])
    score_percentage = score / len(correct_answers)

    return model_response, score_percentage

