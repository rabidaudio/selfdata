{{
  config(
    external_location = target.get('s3_staging_dir') + "data/listening_clock",
    materialized = 'table',
  )
}}
with _ref_scrobbles as (
  select * from {{ ref('scrobbles') }}
),

_ref_users as (
  select * from {{ ref('lastfm_users') }}
),

recent_scrobbles as (
  select
    u.username,
    hour(at_timezone(scrobbled_at, coalesce(u.timezone, 'America/New_York'))) as hour_of_day
  from _ref_scrobbles s
  inner join _ref_users u on u.username = s.username
  -- using scrobbled_at_year to get partitioning, then subfiltering to 6M
  where date(s.scrobbled_at_year) = date_trunc('year', now() - interval '1' year)
    and s.scrobbled_at > now() - interval '6' month
),

scrobble_counts_by_hour as (
  select
    username,
    hour_of_day,
    count(*) as scrobble_count
  from recent_scrobbles
  group by username, hour_of_day
),

all_rows as (
  select
    h.hour_of_day,
    u.username
  from _ref_users as u
  cross join UNNEST(SEQUENCE(0,23)) as h(hour_of_day)
),

absolute_scrobble_counts_for_all_rows as (
  select
    r.username,
    r.hour_of_day,
    coalesce(s.scrobble_count, 0) as scrobble_count
  from all_rows as r
  left join scrobble_counts_by_hour as s
    on s.hour_of_day = r.hour_of_day and r.username = s.username
),

relative_scrobble_counts as (
  select
    username,
    hour_of_day,
    scrobble_count as absolute_plays,
    cast(scrobble_count as double) /
      cast(nullif(sum(scrobble_count) over (partition by username), 0) as double) as relative_plays
  from absolute_scrobble_counts_for_all_rows
  order by username, hour_of_day
)

select * from relative_scrobble_counts
