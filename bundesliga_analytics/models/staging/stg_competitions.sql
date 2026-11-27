--stg_competitions.sql 

with source as (
    SELECT * FROM {{ source('football_data', 'competitions') }}
    ),

renamed as (
    SELECT 
    id as competition_id,
    name as competition_name,
    code as competition_code,
    type as competition_type,
    emblem
    FROM source
)

SELECT * FROM renamed