--dim_competitions.sql 

with source as (
    SELECT * FROM {{ ref('stg_competitions') }}
),


dim_competitions as (
    SELECT
        source.competition_id,
        source.competition_code,
        source.competition_name,
        source.competition_type,
        source.emblem
    FROM source
)

SELECT * FROM dim_competitions