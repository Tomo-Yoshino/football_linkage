import requests
import json

uri = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'e2b30186b16b46b98e75d4a11fc5f8ff' }

response = requests.get(uri, headers=headers)
for match in response.json()['matches']:
  print(match)