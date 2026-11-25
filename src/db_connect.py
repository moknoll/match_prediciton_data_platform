import os

import psycopg2
from dotenv import load_dotenv


def load_in_db(teams: dict, seasons: dict, matches: dict):

    load_dotenv()
    try:
        conn = psycopg2.connect(host=os.getenv("POSTGRES_HOST"), 
                            port=os.getenv("POSTGRES_PORT"), 
                            dbname=os.getenv("POSTGRES_DB"),
                            user=os.getenv("POSTGRES_USER"), 
                            password=os.getenv("POSTGRES_PASSWORD"))
        print("Database connected successfully")
    except psycopg2.OperationalError: 
        print("Could not connect to Database")
        return

    cur = conn.cursor()

    for key, value in teams.items():         
            team_id = key
            name = value["name"]
            tla = value["tla"]
            crest = value["crest"]
            short_name = value["shortName"]
            
            # executing queries to create table
            try: 
                cur.execute(
                    "INSERT INTO teams (id, name, tla, crest, short_name) " \
                    "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) " \
                    "DO UPDATE SET\
                       name = EXCLUDED.name,\
                       tla = EXCLUDED.tla, \
                       crest = EXCLUDED.crest, \
                       short_name = EXCLUDED.short_name",
                    (team_id, name, tla, crest, short_name)
                )
    
            except psycopg2.DatabaseError as error:
                print(error)
                conn.rollback()
                return

    for key, value in seasons.items():
        season_id = key
        competition_id = value["competition_id"]
        start_date = value["start_date"]
        end_date = value["end_date"]
        winner_team_id = value["winner_team_id"]
        try:
            cur.execute(
                    "INSERT INTO seasons (id, competition_id, start_date, end_date, winner_team_id)" \
                    "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) "\
                    "DO UPDATE SET\
                        competition_id = EXCLUDED.competition_id,\
                        start_date = EXCLUDED.start_date, \
                        end_date = EXCLUDED.end_date, \
                        winner_team_id = EXCLUDED.winner_team_id",
                        (season_id, competition_id, start_date, end_date, winner_team_id)                           
                    )
        except psycopg2.DatabaseError as error:
            print(error)
            conn.rollback()
            return

    for key, value in matches.items():
        match_id = key
        utc_date = value["utc_date"]
        home_team_id = value["home_team_id"]
        away_team_id = value["away_team_id"]
        score_fulltime_home = value["score_fulltime_home"]
        score_fulltime_away = value["score_fulltime_away"]
        score_halftime_home = value["score_halftime_home"]
        score_halftime_away = value["score_halftime_away"]
        winner = value["winner"]
        season_id = value["season_id"]
        status = value["status"]
        last_updated = value["last_updated"]
        matchday = value["matchday"]


        try:
            cur.execute(
                """
                INSERT INTO matches (
                    id,
                    utc_date,
                    home_team_id,
                    away_team_id,
                    score_fulltime_home,
                    score_fulltime_away,
                    score_halftime_home,
                    score_halftime_away,
                    winner,
                    season_id,
                    status,
                    matchday,
                    last_updated
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (id)
                DO UPDATE SET
                    utc_date = EXCLUDED.utc_date,
                    home_team_id = EXCLUDED.home_team_id,
                    away_team_id = EXCLUDED.away_team_id,
                    score_fulltime_home = EXCLUDED.score_fulltime_home,
                    score_fulltime_away = EXCLUDED.score_fulltime_away,
                    score_halftime_home = EXCLUDED.score_halftime_home,
                    score_halftime_away = EXCLUDED.score_halftime_away,
                    winner = EXCLUDED.winner,
                    season_id = EXCLUDED.season_id,
                    status = EXCLUDED.status,
                    matchday = EXCLUDED.matchday,
                    last_updated = EXCLUDED.last_updated
                """,
                (
                    match_id,
                    utc_date,
                    home_team_id,
                    away_team_id,
                    score_fulltime_home,
                    score_fulltime_away,
                    score_halftime_home,
                    score_halftime_away,
                    winner,
                    season_id,
                    status,
                    matchday,
                    last_updated
                )
            )
        except psycopg2.DatabaseError as error:
            print(error)
            conn.rollback()
            return
    conn.commit()            
    # cur.execute(
    # "SELECT * FROM teams;"

    # )
    # rows = cur.fetchall()
    # for row in rows: 
    #     print(row)

    cur.close()
    conn.close()
