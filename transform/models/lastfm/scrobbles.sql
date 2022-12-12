-- Ideally this would be partitioned by both month and username for
-- performance. However, with Athena basically you can't insert
-- more than 100 partitions per query (HIVE_TOO_MANY_OPEN_PARTITIONS).

-- insert_by_period is a workaround for this sort of problem, but it
-- doesn't work with Athena currently.
-- For now, we're partitioning by user and year. Eventually we'll hit
-- the limit again.
-- 
-- 
-- see:
-- https://docs.aws.amazon.com/athena/latest/ug/troubleshooting-athena.html#troubleshooting-athena-create-table-as-select-ctas
-- https://github.com/dbt-athena/dbt-athena/issues/87
-- https://github.com/dbt-labs/dbt-labs-experimental-features/tree/main/insert_by_period
-- 
-- Currently the whole data set is only 26MB, perhaps partitioning is pointless...
{{
  config(
    materialized = 'incremental',
    partitioned_by = ['scrobbled_at_year', 'username'],
  )
}}
with _src_scrobbles as (
  select * from {{ source('tap_lastfm', 'scrobbles') }}
  {% if is_incremental() %}
    -- where dt >= (select max(dt) from {{ this }})
    where date(dt) >= (select max(date(scrobbled_at_year)) from {{ this }})
  {% endif %}
),

_unique_scrobbles as (
  {{ distinct_on('_src_scrobbles', ['username', 'date']) }}
),

scrobbles as (
  select
    cast("date" as timestamp) as scrobbled_at,
    name as track_name,
    nullif(json_extract_scalar(artist, '$.name'), 'null') as artist_name,
    nullif(json_extract_scalar(album, '$.name'), 'null') as album_name,
    mbid as musicbrainz_track_id,
    nullif(json_extract_scalar(artist, '$.mbid'), 'null') as musicbrainz_artist_id,
    nullif(json_extract_scalar(album, '$.mbid'), 'null') as musicbrainz_release_id,
    loved as is_loved,
    -- partition columns must come at end
    cast(cast(date_trunc('year', cast("date" as timestamp)) as date) as varchar) as scrobbled_at_year,
    username
  from _unique_scrobbles
  order by username asc, scrobbled_at desc
)

select * from scrobbles
