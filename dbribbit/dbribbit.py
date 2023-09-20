import requests
import pymongo
import time
import logging
import os 

# Set the logging level
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# URL of the PondPulse microservice
pondpulse_url = "http://pondpulse:5000/microservices"
#db_user = os.getenv('YOUR_ENV_VARIABLE_NAME')// to implement when deploying to k8s
#db_pass = os.getenv('YOUR_ENV_VARIABLE_NAME')// to implement when deploying to k8s

# Initialize a connection to MongoDB
mongo_client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")  # Replace with your MongoDB connection string
db = mongo_client["faulty_versions_db"]  # Replace with your database name
collection = db["faulty_versions"]

# Function to poll PondPulse and persist faulty versions to MongoDB
def poll_and_persist_faulty_versions():
    try:
        response = requests.get(pondpulse_url)
        response.raise_for_status()
        microservices_data = response.json()

        # Check the state of each microservice
        for microservice, data in microservices_data.items():
            if data['state'] in ['insecure', 'slow']:
                logging.info(f"found a faulty microservice {microservice}")
                # Persist the faulty version to MongoDB
                faulty_version = {
                    "microservice": microservice,
                    "version": data['version'],
                    "state": data['state'],
                    "timestamp": int(time.time())
                }
                logging.info(f"writing to DB - {faulty_version}")
                collection.insert_one(faulty_version)
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to PondPulse: {str(e)}")

if __name__ == '__main__':
    while True:
        poll_and_persist_faulty_versions()
        time.sleep(30)  # Poll every 30 minutes (adjust the interval as needed)
