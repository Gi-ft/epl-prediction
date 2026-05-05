from fetch_data import teams_data, standings_data, matches_data
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:13097.Lr@localhost/epl_database")

# Inserting Team Data
for team in teams_data['teams']:
    team_id = team['id']
    name = team['name']

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT IGNORE INTO teams (team_id, name)
            VALUES (:team_id, :name)
        """), {"team_id": team_id, "name": name})

#Inserting Standings
# Clear existing data to ensure fresh insert with all columns
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE standings"))

for team in standings_data['standings'][0]['table']:
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO standings (
                team_id, position, played, won, draw, lost, points, goal_difference, goals_for, goals_against
            )
            VALUES (:team_id, :position, :played, :won, :draw, :lost, :points, :goal_difference, :goals_for, :goals_against)
        """), {
            "team_id": team['team']['id'],
            "position": team['position'],
            "played": team['playedGames'],
            "won": team['won'],
            "draw": team['draw'],
            "lost": team['lost'],
            "points": team['points'],
            "goal_difference": team['goalDifference'],
            "goals_for": team['goalsFor'],
            "goals_against": team['goalsAgainst']
        })

#Insert matches 
for match in matches_data['matches']:
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT IGNORE INTO matches (
                match_id, match_date,
                home_team_id, away_team_id,
                home_goals, away_goals, status
            )
            VALUES (:match_id, :match_date, :home_team_id, :away_team_id,
                    :home_goals, :away_goals, :status)
        """), {
            "match_id": match['id'],
            "match_date": match['utcDate'],
            "home_team_id": match['homeTeam']['id'],
            "away_team_id": match['awayTeam']['id'],
            "home_goals": match['score']['fullTime']['home'],
            "away_goals": match['score']['fullTime']['away'],
            "status": match['status']
        })

