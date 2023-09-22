from flask import Flask, request, jsonify
import random
import json
import logging
import os 

# Set the logging level
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Dummy data for the 5 microservices
microservices_data = {
    'Frog1': {'version': 1, 'state': 'healthy'},
    'Frog2': {'version': 1, 'state': 'healthy'},
    'Frog3': {'version': 1, 'state': 'healthy'},
    'Frog4': {'version': 1, 'state': 'healthy'},
    'Frog5': {'version': 1, 'state': 'healthy'}
}

# Function to randomly update the version and state of a microservice
def generate_microservice_data():
    for microservice in microservices_data:
        # Randomly increment the version
        microservices_data[microservice]['version'] += random.randint(1, 3)
    return microservices_data

# Function to update microservice data
def update_microservice_data(updated_data):
    for microservice, data in updated_data.items():
        if microservice in microservices_data:
            microservices_data[microservice] = data


@app.route('/microservices', methods=['GET'])
def get_microservices_data():
    return jsonify(generate_microservice_data())

@app.route('/microservices/update', methods=['POST'])
def update_microservices():
    try:
        updated_data = request.json
        update_microservice_data(updated_data)
        return jsonify({'message': 'Microservices data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
