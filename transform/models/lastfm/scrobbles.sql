{{
  config(
    materialized = 'incremental',
    partitioned_by = ['scrobbled_at_month', 'username'],
  )
}}
with _src_scrobbles as (
  select * from {{ source('tap_lastfm', 'scrobbles') }}
  {% if is_incremental() %}
    -- where dt >= (select max(dt) from {{ this }})
    where date(dt) >= (select max(date(scrobbled_at_month)) from {{ this }})
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
    cast(cast(date_trunc('month', cast("date" as timestamp)) as date) as varchar) as scrobbled_at_month,
    username
  from _unique_scrobbles
  order by username asc, scrobbled_at desc
)

select * from scrobbles
