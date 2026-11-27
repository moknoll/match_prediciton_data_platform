--int_seasons_enriched.sql 

WITH competition AS (
    -- stg_matches referenzieren
    select * from {{ ref('stg_competitions') }}
),


seasons AS (
    -- stg_seasons referenzieren
    select * from {{ ref('stg_seasons') }}
),

joined AS (
    -- die Daten miteinander verbinden
    SELECT
        seasons.season_id,
        seasons.start_date,
        seasons.end_date,
        seasons.winner_team_id,
        competition.competition_code AS competition_code,
        competition.competition_name AS competition_name,
        competition.competition_id AS competition_id
    FROM seasons

    left join competition 
        ON competition.competition_id = seasons.competition_id
)

SELECT *
FROM joined