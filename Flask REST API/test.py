# Module to handle HTTP requests
import requests

# Defines base URL of locally run Flask server (at port 5000) - endpoint for HTTP requests
BASE = "http://127.0.0.1:5000/"

# List containing dictionaries, representing student information
data = [{"name": "james smith", "degree": "english", "grade": 75,},
        {"name": "michael revolt", "degree": "history", "grade": 86},
        {"name": "richard galluci", "degree": "maths", "grade": 68}]

# Retrieve and print each student's information from data list in JSON format
for i in range(len(data)): # Loops through all student data in list
    response = requests.put(BASE + "students/" + str(i), json=data[i]) # Sends PUT request to Flask server in JSON format
    print(response.json()) # Prints server response in JSON format

response = requests.get(BASE + "students/1") # Sends GET request to Flask server
print(response.json())  # Prints server response in JSON format
input() # Pause for user input (to check output before proceeding)

response = requests.delete(BASE + "students/2") # Sends DELETE request to Flask server
print(response.status_code) # Prints server response (status code)
input() # Pause for user input (to check output before proceeding)

response = requests.patch(BASE + "students/0", json={"grade": 100}) # Sends PATCH request (update grade) to Flask server in JSON format
print(response.json()) # Prints server response in JSON format
