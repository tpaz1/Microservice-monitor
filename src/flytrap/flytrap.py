import requests
import time
import random
import logging
import os 

# Set the logging level
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

# URL of the PondPulse microservice
pondpulse_url = "http://pondpulse-service:5000/microservices"

# setting a maximum retry cycles
max_retries = 3

# Function to check the health of microservices
def check_microservices_health():
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(pondpulse_url)
            #response.raise_for_status()
            microservices_data = response.json()

            # Check the state of each microservice
            for microservice, data in microservices_data.items():
                # Simulate detecting a bug
                if should_detect_bug():
                    new_state = random.choice(['insecure', 'slow', 'healthy'])
                    logging.debug(f"Detected bug in {microservice}. Modifying state to {new_state}.")
                    data['state'] = new_state
                else:
                    logging.debug(f"No issues found in {microservice}.")

            # Send the updated data back to PondPulse
            response = requests.post(pondpulse_url + '/update', json=microservices_data)
            response.raise_for_status()
            logging.info("Microservices data updated successfully.")

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

# Function to simulate bug detection with a low (random) frequency
def should_detect_bug():
    return random.random() < 0.25  # Adjust the frequency as needed

if __name__ == '__main__':
    while True:
        check_microservices_health()
        time.sleep(60)  # Check every 1 minutes (adjust the interval as needed)
