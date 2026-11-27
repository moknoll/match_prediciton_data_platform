--stg_seasons.sql 

with source as (
    SELECT * FROM {{ source('football_data', 'seasons') }}
    ),

renamed as (
    SELECT 
    id as season_id,
    competition_id,
    start_date, 
    end_date,
    winner_team_id
    FROM source
)

SELECT * FROM renamed