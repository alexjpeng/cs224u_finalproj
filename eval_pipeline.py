from LLMMathBaseline import LLMMathBaseline
import json
import os


model = LLMMathBaseline()

def ensure_predictions_directory_exists():
    # Check if the predictions directory exists, if not create it
    if not os.path.exists('predictions'):
        os.mkdir('predictions')

def query_model_and_save_prediction(record):
    # Initialize the model
    model = LLMMathBaseline()
    pre_text = record['pre_text']
    table = record['table']
    post_text = record['post_text']
    question = record['qa']['question']

    # Combining pre_text, post_text and table to create the context
    context = '\n'.join(pre_text + post_text)
    if table:
        context += '\n' + '\n'.join([' '.join([str(cell) for cell in row]) for row in table])

    # Query the model
    prediction = model.query(question, context)

    # Save prediction to a file
    prediction['id'] = record['id']
    with open('predictions/predictions.json', 'a') as f:
        f.write(json.dumps(prediction) + '\n')




# Read test.json from FinQA/dataset and print each record to console
with open('FinQA/dataset/test.json', 'r') as f:
    test_data = json.load(f)

# Executing the pipeline
ensure_predictions_directory_exists()
for record in test_data:
    query_model_and_save_prediction(record)