--stg_matches.sql 

with source as (
    SELECT * FROM {{ source('football_data', 'matches') }}
    ),

renamed as(
    SELECT
    
    --------ids
    id as match_id,

    utc_date,
    matchday,
    home_team_id,
    away_team_id, 
    score_fulltime_away,
    score_fulltime_home,
    score_halftime_away,
    score_halftime_home,
    winner as match_winner, 
    season_id,
    status as match_status,
    last_updated

    FROM source
)

SELECT * FROM renamed