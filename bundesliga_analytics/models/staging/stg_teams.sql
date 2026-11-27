--stg_teams.sql

with source as (
    SELECT * FROM {{ source('football_data', 'teams') }}
    ),

renamed as(
    SELECT 
    id as team_id, 
    name as team_name,
    short_name, 
    tla,
    crest
    FROM source
)

SELECT * FROM renamed