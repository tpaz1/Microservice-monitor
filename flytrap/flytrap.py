import requests
import time
import random

# URL of the PondPulse microservice
pondpulse_url = "http://127.0.0.1:5000/microservices"

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
                    print(f"Detected bug in {microservice}. Modifying state to 'insecure'.")
                    data['state'] = random.choice(['insecure', 'slow'])
                else:
                    print(f"No issues found in {microservice}.")

        # Send the updated data back to PondPulse
        print(microservices_data)
        print(type(microservices_data))
        response = requests.post(pondpulse_url + '/update', json=microservices_data)
        response.raise_for_status()
        print("Microservices data updated successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to PondPulse: {str(e)}")

# Function to simulate bug detection with a low (random) frequency
def should_detect_bug():
    return random.random() < 0.5  # Adjust the frequency as needed

if __name__ == '__main__':
    while True:
        check_microservices_health()
        time.sleep(30)  # Check every 5 minutes (adjust the interval as needed)
