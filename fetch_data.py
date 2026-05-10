import os

import requests


api_token = os.getenv("FOOTBALL_DATA_API_KEY")

if not api_token:
    raise RuntimeError(
        "FOOTBALL_DATA_API_KEY is not set. Add it as an environment variable "
        "or Streamlit secret before fetching data."
    )

headers = {"X-Auth-Token": api_token}

# Fetch Teams
teams_url = "https://api.football-data.org/v4/competitions/PL/teams"
teams_response = requests.get(teams_url, headers=headers)
teams_data = teams_response.json()

# Fetch Standings
standings_url = "https://api.football-data.org/v4/competitions/PL/standings"
standings_response = requests.get(standings_url, headers=headers)
standings_data = standings_response.json()
import json
print(json.dumps(standings_data['standings'][0]['table'], indent=2))


# Fetch Matches
matches_url = "https://api.football-data.org/v4/competitions/PL/matches"
matches_response = requests.get(matches_url, headers=headers)
matches_data = matches_response.json()
