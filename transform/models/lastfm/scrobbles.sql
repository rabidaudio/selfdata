with _src_scrobbles as (
  select * from {{ source('tap_lastfm', 'scrobbles') }}
),

scrobbles as (
  SELECT
    {{ eastern_time('date') }} as scrobbled_at,
    username,
    name as track_name,
    artist__name as artist_name,
    album__name as album_name,
    mbid as musicbrainz_track_id,
    artist__mbid as musicbrainz_artist_id,
    album__mbid as musicbrainz_release_id,
    loved as is_loved
  FROM _src_scrobbles
  order by username, scrobbled_at desc
)

select * from scrobbles
