--dim_teams.sql 

WITH source AS (
    -- stg_matches referencing
    select * from {{ ref('stg_teams') }}
),

dim_teams as (
    SELECT 
        source.team_id,
        source.team_name,
        source.short_name,
        source.tla,
        source.crest
    FROM source
)

SELECT * FROM dim_teams