import json
import os
import re

predictions = []
with open('predictions/predictions-answerWithTextbook.json') as f:
  for line in f:
    data = json.loads(line)
    predictions.append(data)


with open('FinQA/dataset/test.json') as f2:
  test_data = json.load(f2)

num_correct = 0

def extract_number(s):
    # Extracts a number from a string
    # Example: "658 (million)" => "658"
    match = re.search(r"[-+]?\d*\.\d+|\d+", s)
    return float(match.group()) if match else None

def convert_percentage_to_fraction(num, s):
    # Converts a percentage to fraction if "%" is present in the string
    # Example: 13.39 => 0.1339
    return num / 100 if '%' in s else num


def evaluate_predictions(test_data, predictions):
    num_correct = 0

    for record in test_data:
        for prediction in predictions:
            if prediction['id'] == record['id']:
                ans = prediction['answer']
                temp = num_correct
                ans = ans.replace('$', '')

                if 'y' in ans.lower() and ('y' in str(record['qa']['exe_ans']).lower() or 't' in str(record['qa']['exe_ans']).lower()):
                    num_correct += 1
                elif 'n' in ans.lower() and ('n' in str(record['qa']['exe_ans']).lower() or 'f' in str(record['qa']['exe_ans']).lower()):
                    num_correct += 1
                elif ans == str(record['qa']['exe_ans']):
                    num_correct += 1    

                # Extract numerical values
                predicted_num = extract_number(ans)
                actual_num = extract_number(str(record['qa']['exe_ans']))

                # Convert percentage to fraction if "%" is in the string
                if actual_num is not None and predicted_num is not None:
                    predicted_num = convert_percentage_to_fraction(predicted_num, ans)
                    actual_num = convert_percentage_to_fraction(actual_num, str(record['qa']['exe_ans']))
                    
                    # Compare numbers with a tolerance, you can adjust this as needed
                    if abs(predicted_num - actual_num) < 2:
                        num_correct += 1
                        break
                else:
                  if ans == 'error':
                    break
                if temp == num_correct:
                  print("Question: ", record['qa']['question'])
                  print("Answer: ", record['qa']['exe_ans'])
                  print("Prediction: ", ans)
                    
    # Return number of correct predictions
    return num_correct

# Example usage:
num_correct = evaluate_predictions(test_data, predictions)
print(f"Number of correct predictions: {num_correct}")



print("Accuracy: ", num_correct/(len(test_data)))



