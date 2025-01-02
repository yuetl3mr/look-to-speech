from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    response = requests.post('http://127.0.0.1:8000/predict', json={"data": "some_data"})
    result = response.json()
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)