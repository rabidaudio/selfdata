with _ref_scrobbles as (
  select * from {{ ref('scrobbles') }}
),

_ref_users as (
  select * from {{ ref('lastfm_users') }}
),

all_usernames as (
  select username from _ref_users
),

recent_scrobbles as (
  select
    username,
    scrobbled_at
  from _ref_scrobbles
  where scrobbled_at > now() - interval '6 months'
),

all_rows as (
  select
    h.hour_of_day,
    u.username
  from all_usernames as u
  cross join generate_series(0, 23) as h(hour_of_day)
),

absolute_scrobble_counts as (
  select
    username,
    extract(hour from scrobbled_at)::integer as hour_of_day,
    count(*) as scrobble_count
  from recent_scrobbles
  group by username, hour_of_day
),

absolute_scrobble_counts_for_all_rows as (
  select
    r.username,
    r.hour_of_day,
    coalesce(s.scrobble_count, 0) as scrobble_count
  from all_rows as r
  left join absolute_scrobble_counts as s
    on s.hour_of_day = r.hour_of_day and r.username = s.username
),

relative_scrobble_counts as (
  select
    username,
    hour_of_day,
    scrobble_count as absolute_plays,
    coalesce(
      nullif(scrobble_count::decimal, 0)
      / nullif(
        sum(scrobble_count) over (partition by username),
        0), 0
    ) as relative_plays
  from absolute_scrobble_counts_for_all_rows
  order by username, hour_of_day
)

select * from relative_scrobble_counts
