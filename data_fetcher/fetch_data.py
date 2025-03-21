import requests

api_key = "e547ef531e5848919c3dfe43d910d435"
url = "https://api.football-data.org/v4/competitions/PL/matches"

headers = {
    "X-Auth-Token": api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data. Error code: {response.status_code}")

