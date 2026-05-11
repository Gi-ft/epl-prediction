import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BASE_URL = "https://api.football-data.org/v4"

HEADERS = {"X-Auth-Token": API_KEY}


def fetch_teams():
    """Fetch all teams in the Premier League."""
    url = f"{BASE_URL}/competitions/PL/teams"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def fetch_standings():
    """Fetch current Premier League standings."""
    url = f"{BASE_URL}/competitions/PL/standings"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def fetch_matches():
    """Fetch all matches for the current Premier League season."""
    url = f"{BASE_URL}/competitions/PL/matches"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


# Fetch data on module import
teams_data = fetch_teams()
standings_data = fetch_standings()
matches_data = fetch_matches()
