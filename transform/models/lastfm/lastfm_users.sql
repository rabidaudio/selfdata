with _src_users as (
  -- don't query all the back partitions since we only care about the most recent data
  {{ most_recent_version(source('tap_lastfm', 'users')) }}
),

_ref_user_timezones as (
  select * from {{ ref('lastfm_user_timezones') }}
),

_distinct_users as (
  {{ distinct_on('_src_users', ['username']) }}
),

lastfm_users as (
  select
    u.username,
    u.realname as full_name,
    u.url,
    u.country,
    u.age,
    u.gender,
    u.subscriber as is_subscriber,
    u.registered_at as registered_at,
    ut.timezone as timezone
  from _distinct_users u
  left join _ref_user_timezones ut on ut.username = u.username
)

select * from lastfm_users
