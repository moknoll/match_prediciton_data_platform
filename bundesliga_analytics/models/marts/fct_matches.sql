--fct_matches.sql

WITH matches as (
    select * from {{ ref("int_matches_enriched")}}
),

fct_matches as (
    SELECT 
        matches.match_id,
        matches.season_id,
        matches.competition_id,
        matches.matchday, 
        matches.date,
        matches.home_team_id,
        matches.away_team_id,
        matches.home_goals,
        matches.away_goals,
        matches.match_status,
        matches.match_winner

    FROM
        matches
)

SELECT * from fct_matches