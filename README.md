# EPL 2025/26 Prediction Model

A Python-based prediction system for the English Premier League title race, using Monte Carlo simulation to forecast final standings based on team strength metrics.

## Overview

This project fetches live Premier League data from the [football-data.org API](https://www.football-data.org/), stores it in a PostgreSQL database using SQLAlchemy, and runs Monte Carlo simulations to predict the probability of each team winning the league title.

## Features

- **Data Pipeline**: Fetches teams, standings, and match data from football-data.org
- **Database Storage**: PostgreSQL backend using SQLAlchemy
- **Team Strength Calculation**: 
  - Points per game (PPG)
  - Goal difference per game
  - Recent form (last 5 matches)
- **Monte Carlo Simulation**: 10,000+ simulations of remaining fixtures
- **Title Race Analysis**: Focus on Arsenal vs Manchester City probability

## Project Structure

```
.
├── fetch_data.py          # API data fetching
├── postgres_connector.py  # Database insertion for PostgreSQL (SQLAlchemy)
├── model_simulation.ipynb # Main simulation notebook
├── viualization.ipynb     # Visualization notebook
├── requirements.txt       # Python dependencies
└── .gitignore            # Git exclusions
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- sqlalchemy
- psycopg
- pandas
- requests
- matplotlib (for visualization)

### 2. Configure Database

Set a PostgreSQL connection string before running the loader:

```bash
$env:DATABASE_URL="postgresql+psycopg://postgres:password@localhost:5432/epl_database"
```

### 3. Set up PostgreSQL Schema

```sql
CREATE DATABASE epl_database;

CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE standings (
    team_id INT PRIMARY KEY,
    position INT,
    played INT,
    won INT,
    draw INT,
    lost INT,
    points INT,
    goal_difference INT,
    goals_for INT,
    goals_against INT
);

CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    match_date TIMESTAMP,
    home_team_id INT,
    away_team_id INT,
    home_goals INT,
    away_goals INT,
    status VARCHAR(20)
);
```

### 4. API Key

Set your football-data.org API key in `fetch_data.py`:

```python
headers = {"X-Auth-Token": "your-api-key-here"}
```

Get a free API key at [football-data.org](https://www.football-data.org/).

## Usage

### Step 1: Fetch and Store Data

```bash
python fetch_data.py
python postgres_connector.py
```

### Step 2: Run Simulation

Open `model_simulation.ipynb` in Jupyter and run all cells:

```bash
jupyter notebook model_simulation.ipynb
```

The notebook will:
1. Load current standings from PostgreSQL
2. Calculate team strength metrics
3. Run 10,000 simulations of remaining matches
4. Output title win probabilities

### Step 3: Visualize Results

Use `viualization.ipynb` to create charts and distributions.

## Simulation Methodology

### Team Strength Formula
```
strength = 0.5 * ppg + 0.3 * (gd_pg) + 0.2 * form
```

### Match Simulation
- Home advantage factor: 1.1x
- Win probability based on relative team strength
- Draw probability: fixed 20%

### Example Output
```
Arsenal win %: 57.52
Man City win %: 32.33
```

## Data Flow

```
football-data.org API
        ↓
   fetch_data.py
        ↓
 PostgreSQL Database
        ↓
model_simulation.ipynb
        ↓
  Predictions/Visuals
```

## License

MIT

## Acknowledgments

- Data provided by [football-data.org](https://www.football-data.org/)
