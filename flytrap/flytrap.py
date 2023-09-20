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
pondpulse_url = "http://pondpulse:5000/microservices"

# Function to check the health of microservices
def check_microservices_health():
    try:
        response = requests.get(pondpulse_url)
        response.raise_for_status()
        microservices_data = response.json()

        # Check the state of each microservice
        for microservice, data in microservices_data.items():
            if data['state'] == 'healthy':
                # Simulate detecting a bug
                if should_detect_bug():
                    new_state = random.choice(['insecure', 'slow'])
                    logging.debug(f"Detected bug in {microservice}. Modifying state to {new_state}.")
                    data['state'] = new_state
                else:
                    logging.debug(f"No issues found in {microservice}.")

        # Send the updated data back to PondPulse
        response = requests.post(pondpulse_url + '/update', json=microservices_data)
        response.raise_for_status()
        logging.info("Microservices data updated successfully.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to PondPulse: {str(e)}")

# Function to simulate bug detection with a low (random) frequency
def should_detect_bug():
    return random.random() < 0.1  # Adjust the frequency as needed

if __name__ == '__main__':
    while True:
        check_microservices_health()
        time.sleep(60)  # Check every 1 minutes (adjust the interval as needed)
