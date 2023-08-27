from flask import Flask, jsonify, render_template
from collections import deque
import json

app = Flask(__name__)

#checks if its already existing , if so reads the file upto 20 records 
try:
    with open('operation_history.json', 'r') as file:
        operation_history = deque(json.load(file), maxlen=20)
except FileNotFoundError:
    # Store operation history with a maximum length of 20
    operation_history = deque(maxlen=20)

#saves the operation in a local json file - task (d) completed
def save_operation_history():
    with open('operation_history.json', 'w') as file:
        json.dump(list(operation_history), file)

#evaluvation function
def evaluate_expression(expression):
    try:
        return eval(expression)
    except Exception:
        raise ValueError("Invalid operation")

#routing to the home page - HTML
@app.route('/')
def index():
    return render_template('index.html')
    
#routing history
@app.route('/history')
def get_history():
    history_list = list(operation_history)
    return jsonify(history_list)

# routing operation path
@app.route('/<path:operation>')
def calculate(operation):
    parts = operation.split('/')
    
    # Replace operation keywords with operators
    for i in range(len(parts)):
        if parts[i] == 'into':
            parts[i] = '*'
        elif parts[i] == 'plus':
            parts[i] = '+'
        elif parts[i] == 'minus':
            parts[i] = '-'    
    
    # Construct the expression
    expression = ''.join(parts)
    
    try:
        result = evaluate_expression(expression)
        question = ''.join(parts)
        
        # creating the answer in dict which is being converted to json
        answer = {'question': question,'answer': result}
        operation_history.append(answer)
        json_object = json.dumps(answer)
        save_operation_history()
        return json_object
    
    #error handling
    except ValueError as e:
        return jsonify({'error': str(e)})

#hosting in localhost:3000
if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)
