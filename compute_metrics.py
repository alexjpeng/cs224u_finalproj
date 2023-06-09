import json
import os

predictions = []
with open('predictions/predictions1.json') as f:
  for line in f:
    data = json.loads(line)
    predictions.append(data)


with open('FinQA/dataset/test.json') as f2:
  test_data = json.load(f2)

num_correct = 0

for record in test_data:
    for prediction in predictions:
        if prediction['id'] == record['id'] and prediction['answer'] == record['qa']['answer']:
            num_correct += 1
            break


print("Accuracy: ", num_correct/len(predictions))



