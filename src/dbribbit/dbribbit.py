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
pondpulse_url = "http://pondpulse-service:5000/microservices"
db_user = os.getenv('ME_CONFIG_MONGODB_ADMINUSERNAME') 
db_pass = os.getenv('ME_CONFIG_MONGODB_ADMINPASSWORD')
mongo_url = os.getenv('ME_CONFIG_MONGODB_SERVER')

# Initialize a connection to MongoDB
mongo_client = pymongo.MongoClient("mongodb://admin:admin@mongodb-service:27017/")  # Replace with your MongoDB connection string
db = mongo_client["faulty_versions_db"]  # Replace with your database name
collection = db["faulty_versions"]

# setting a maximum retry cycles
max_retries = 3

# Function to poll PondPulse and persist faulty versions to MongoDB
def poll_and_persist_faulty_versions():
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(pondpulse_url)
            #response.raise_for_status()
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
            break
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to PondPulse: {str(e)}")
            retries += 1
            if retries < max_retries:
                logging.info(f"Retrying in 10 seconds...")
                time.sleep(10)
            else:
                logging.warning("Max retry attempts reached. Exiting...")
                break

if __name__ == '__main__':
    while True:
        poll_and_persist_faulty_versions()
        time.sleep(30)  # Poll every 30 minutes (adjust the interval as needed)
