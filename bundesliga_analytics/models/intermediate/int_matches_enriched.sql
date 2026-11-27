--int_matches_enriched.sql 

WITH matches AS (
    -- stg_matches referenzieren
    select * from {{ ref('stg_matches') }}
),

teams AS (
    -- stg_teams referenzieren
    select * from {{ ref('stg_teams') }}
),

seasons AS (
    SELECT * FROM {{ ref('int_seasons_enriched') }}
),

joined AS (
    -- die Daten miteinander verbinden
    SELECT 
        matches.match_id,
        matches.home_team_id,
        matches.away_team_id,
        matches.utc_date AS date,
        matches.score_fulltime_home AS home_goals, 
        matches.score_fulltime_away as away_goals, 
        matches.matchday,
        matches.match_status,
        matches.match_winner,
        home.team_name AS home_team_name,
        away.team_name AS away_team_name,
        seasons.start_date AS season_start,
        seasons.end_date AS season_end,
        seasons.season_id as season_id,
        seasons.competition_id as competition_id,
        seasons.competition_name as competition_name
    FROM matches

    left join teams AS home
        ON home.team_id = matches.home_team_id
    left join teams AS away
        ON away.team_id = matches.away_team_id
    left join seasons 
        ON seasons.season_id = matches.season_id
)

SELECT *
FROM joined