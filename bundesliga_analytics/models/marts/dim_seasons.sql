--dim_seasons.sql 

WITH source AS (
    -- stg_seasons referenzieren
    select * from {{ ref('stg_seasons') }}
),

dim_seasons as (
    SELECT 
        source.season_id,
        source.start_date,
        source.end_date,
        source.winner_team_id,
        source.competition_id 
    FROM source
)

SELECT * FROM dim_seasons