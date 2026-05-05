import requests


headers = {"X-Auth-Token": "9944c10a5a724cb5884ab9ae5ecde88c"}

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
