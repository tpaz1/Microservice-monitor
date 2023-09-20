import requests
import pymongo
import time

# URL of the PondPulse microservice
pondpulse_url = "http://localhost:5000/microservices"

# Initialize a connection to MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
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
                # Persist the faulty version to MongoDB
                faulty_version = {
                    "microservice": microservice,
                    "version": data['version'],
                    "timestamp": int(time.time())
                }
                collection.insert_one(faulty_version)
    
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to PondPulse: {str(e)}")

if __name__ == '__main__':
    while True:
        poll_and_persist_faulty_versions()
        time.sleep(1800)  # Poll every 30 minutes (adjust the interval as needed)
