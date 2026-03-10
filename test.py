import requests
import json

# Function to get access token using username and password
def get_access_token(username, password, token_url):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
          'username': username,
          'password': password,
          'grant_type': "password",
          'client_id': "acled"
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.status_code} {response.text}")


# Get an access token
my_token = get_access_token(
    username="vvesangi@student.gitam.edu",
    password="Backspace@00005",
    token_url="https://acleddata.com/oauth/token",
)


# Option #1 (parameters in the url)
base_url = "https://acleddata.com/api/acled/read?_format=json&country=Georgia:OR:country=Armenia&year=2021&fields=event_id_cnty|event_date|event_type|country|fatalities"

# request base url with my_token
response = requests.get(
    base_url,
    headers={"Authorization": f"Bearer {my_token}", "Content-Type": "application/json"},
)

if response.json()["status"] == 200:
    print(
        "Request successful"
    )

print(response.json())  # Print the response to see the data

# Option #2 (parameters as a dictionary)
parameters = {
    "country": "Iran:OR:country=Istreal:OR:country=Azerbaijan",
    "year": 2026,
    "fields": "event_id_cnty|event_date|event_type|country|fatalities",
}

response_params_dic = requests.get(
    "https://acleddata.com/api/acled/read?_format=json",
    params=parameters,
    headers={"Authorization": f"Bearer {my_token}", "Content-Type": "application/json"},
)
if response_params_dic.json()["status"] == 200:
    print(
        "Request successful"
    )

print("------------------------------------------------------------------------------------------------------------")
print(response_params_dic.json())  # Print the response to see the data