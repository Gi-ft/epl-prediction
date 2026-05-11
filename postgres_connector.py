import os

from dotenv import load_dotenv
from fetch_data import teams_data, standings_data, matches_data
from sqlalchemy import create_engine, text


load_dotenv()

# Debug: Check what URL was loaded
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL', 'NOT SET')}")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:YOUR_PASSWORD@db.pvvtrlazwhiluzljackj.supabase.co:5432/postgres"
)

print(f"Using URL: {DATABASE_URL[:50]}...")

engine = create_engine(DATABASE_URL)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS standings (
    team_id INTEGER PRIMARY KEY,
    position INTEGER NOT NULL,
    played INTEGER NOT NULL,
    won INTEGER NOT NULL,
    draw INTEGER NOT NULL,
    lost INTEGER NOT NULL,
    points INTEGER NOT NULL,
    goal_difference INTEGER NOT NULL,
    goals_for INTEGER NOT NULL,
    goals_against INTEGER NOT NULL,
    CONSTRAINT fk_standings_team
        FOREIGN KEY (team_id)
        REFERENCES teams (team_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    match_date TIMESTAMPTZ NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    home_goals INTEGER NULL,
    away_goals INTEGER NULL,
    status VARCHAR(20) NOT NULL,
    CONSTRAINT fk_matches_home_team
        FOREIGN KEY (home_team_id)
        REFERENCES teams (team_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_matches_away_team
        FOREIGN KEY (away_team_id)
        REFERENCES teams (team_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_matches_status
    ON matches (status);

CREATE INDEX IF NOT EXISTS idx_matches_match_date
    ON matches (match_date);
"""


def load_data():
    # Debug: Verify which database we're connecting to
    masked_url = DATABASE_URL.replace(DATABASE_URL.split(':')[2].split('@')[0], '***')
    print(f"Connecting to: {masked_url}")

    # Debug: Check if data was fetched
    print(f"Teams data: {len(teams_data.get('teams', []))} teams found")
    print(f"Standings data: {len(standings_data.get('standings', [{}])[0].get('table', []))} standings found")
    print(f"Matches data: {len(matches_data.get('matches', []))} matches found")

    with engine.begin() as conn:
        # Drop existing tables to ensure clean schema
        conn.execute(text("DROP TABLE IF EXISTS matches, standings, teams CASCADE"))
        conn.execute(text(SCHEMA_SQL))

        for team in teams_data["teams"]:
            conn.execute(
                text(
                    """
                    INSERT INTO teams (team_id, name)
                    VALUES (:team_id, :name)
                    """
                ),
                {
                    "team_id": team["id"],
                    "name": team["name"],
                },
            )

        for team in standings_data["standings"][0]["table"]:
            conn.execute(
                text(
                    """
                    INSERT INTO standings (
                        team_id, position, played, won, draw, lost, points, goal_difference, goals_for, goals_against
                    )
                    VALUES (
                        :team_id, :position, :played, :won, :draw, :lost, :points, :goal_difference, :goals_for, :goals_against
                    )
                    """
                ),
                {
                    "team_id": team["team"]["id"],
                    "position": team["position"],
                    "played": team["playedGames"],
                    "won": team["won"],
                    "draw": team["draw"],
                    "lost": team["lost"],
                    "points": team["points"],
                    "goal_difference": team["goalDifference"],
                    "goals_for": team["goalsFor"],
                    "goals_against": team["goalsAgainst"],
                },
            )

        for match in matches_data["matches"]:
            conn.execute(
                text(
                    """
                    INSERT INTO matches (
                        match_id, match_date, home_team_id, away_team_id,
                        home_goals, away_goals, status
                    )
                    VALUES (
                        :match_id, :match_date, :home_team_id, :away_team_id,
                        :home_goals, :away_goals, :status
                    )
                    """
                ),
                {
                    "match_id": match["id"],
                    "match_date": match["utcDate"],
                    "home_team_id": match["homeTeam"]["id"],
                    "away_team_id": match["awayTeam"]["id"],
                    "home_goals": match["score"]["fullTime"]["home"],
                    "away_goals": match["score"]["fullTime"]["away"],
                    "status": match["status"],
                },
            )

    print("Loaded teams, standings, and matches into PostgreSQL.")

    # Show where data is located for pgAdmin verification
    with engine.connect() as conn:
        db_info = conn.execute(text("SELECT current_database(), current_schema()")).fetchone()
        print(f"\nData is in: database='{db_info[0]}', schema='{db_info[1]}'")

        # Count and sample
        counts = conn.execute(text("""
            SELECT 
                (SELECT COUNT(*) FROM teams),
                (SELECT COUNT(*) FROM standings),
                (SELECT COUNT(*) FROM matches)
        """)).fetchone()
        print(f"Table counts: {counts[0]} teams, {counts[1]} standings, {counts[2]} matches")

        print("\nSample teams:")
        for row in conn.execute(text("SELECT * FROM teams LIMIT 5")):
            print(f"  {row.team_id}: {row.name}")


if __name__ == "__main__":
    load_data()
# %%
import os
print(os.getcwd())  # Should show your project folder
print(os.path.exists('.env'))  # Should show True
