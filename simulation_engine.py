import random
from copy import deepcopy

import numpy as np
import pandas as pd


def run_simulation(matches, points, goal_diff, team_strength, simulations=1000):
    team_ids = list(points.keys())
    team_wins = {team: 0 for team in team_ids}

    arsenal_id = 57
    city_id = 65

    arsenal_points_dist = []
    city_points_dist = []
    point_diffs = []

    all_arsenal = []
    all_city = []

    for _ in range(simulations):
        sim_points = deepcopy(points)
        sim_goal_diff = deepcopy(goal_diff)

        sim_progress_a = []
        sim_progress_c = []

        for _, match in matches.iterrows():
            home = match["home_team_id"]
            away = match["away_team_id"]

            home_strength = team_strength.get(home, 1)
            away_strength = team_strength.get(away, 1)

            home_strength *= 1.1
            prob_home = home_strength / (home_strength + away_strength)

            r = random.random()

            if r < prob_home:
                home_goals, away_goals = 2, 1
            elif r < prob_home + 0.2:
                home_goals, away_goals = 1, 1
            else:
                home_goals, away_goals = 1, 2

            if home_goals > away_goals:
                sim_points[home] += 3
            elif home_goals < away_goals:
                sim_points[away] += 3
            else:
                sim_points[home] += 1
                sim_points[away] += 1

            sim_goal_diff[home] += home_goals - away_goals
            sim_goal_diff[away] += away_goals - home_goals

            sim_progress_a.append(sim_points.get(arsenal_id, 0))
            sim_progress_c.append(sim_points.get(city_id, 0))

        arsenal_points_dist.append(sim_points.get(arsenal_id, 0))
        city_points_dist.append(sim_points.get(city_id, 0))
        point_diffs.append(sim_points.get(arsenal_id, 0) - sim_points.get(city_id, 0))

        all_arsenal.append(sim_progress_a)
        all_city.append(sim_progress_c)

        ranked = sorted(sim_points.items(), key=lambda x: x[1], reverse=True)
        winner = ranked[0][0]
        team_wins[winner] += 1

    arsenal_progress = np.mean(all_arsenal, axis=0)
    city_progress = np.mean(all_city, axis=0)

    team_probs = pd.DataFrame(
        {
            "team_id": list(team_wins.keys()),
            "title_probability": [(wins / simulations) * 100 for wins in team_wins.values()],
        }
    ).sort_values("title_probability", ascending=False)

    return {
        "arsenal_points": arsenal_points_dist,
        "city_points": city_points_dist,
        "point_diff": point_diffs,
        "arsenal_progress": arsenal_progress,
        "city_progress": city_progress,
        "team_probs": team_probs,
    }
