import json
from pathlib import Path


def check_dataquality(data: dict) -> bool:

    required_keys = ["id", "name"]
    expected_keys = ["id", "name", "shortName", "tla", "crest"]

    for team in data.values():

        # Required keys: must exist and not be None
        for key in required_keys:
            if key not in team:
                print(f"Missing required key: {key}")
                return False

            if team[key] is None:
                print(f"Required key {key} is None")
                return False

        # Expected keys: missing keys are warnings
        for key in expected_keys:
            if key not in team:
                print(f"Warning: Missing expected key: {key}")
            elif team[key] is None:
                print(f"Warning: {key} is None")
    return True


def parser(years: list[str], league: str) -> dict: 
    p = Path.cwd()
    root = p.parent

    teams = {}
    seasons = {}
    matches = {}
    for year in years:
        data_folder = root / "data" / "raw" / "football_data" / league / year
        
        with (data_folder / f"initial_{year}.json").open('r') as file: 
            data = json.load(file)

        # Parse teams data
        for match in data["matches"]:
            if match["homeTeam"]["id"] not in teams:
                teams[match["homeTeam"]["id"]] = match["homeTeam"]
            if match["awayTeam"]["id"] not in teams: 
                teams[match["awayTeam"]["id"]] = match["awayTeam"]

        # Parse season 
        season =  data["matches"][0]["season"]
        if season["id"] not in seasons:
            seasons[season["id"]] = {
                "competition_id": data["competition"]["id"],
                "start_date": season["startDate"],
                "end_date": season["endDate"],
                "winner_team_id": season["winner"]["id"] if season["winner"] is not None else None
            }

        # Parse match 
        for match in data["matches"]:
            if match["id"] not in matches: 
                matches[match["id"]] = {
                "utc_date": match["utcDate"],
                "matchday": match["matchday"],
                "home_team_id": match["homeTeam"]["id"],
                "away_team_id":  match["awayTeam"]["id"],  
                "score_fulltime_home": match["score"]["fullTime"]["home"],
                "score_fulltime_away": match["score"]["fullTime"]["away"],
                "score_halftime_home": match["score"]["halfTime"]["home"],
                "score_halftime_away": match["score"]["halfTime"]["away"],
                "winner": match["score"]["winner"],
                "season_id": match["season"]["id"],
                "status": match["status"],
                "last_updated": match["lastUpdated"]
            } 

    print(len(matches))
    # print(teams.values())
    # print(len(teams))
    return teams, seasons, matches