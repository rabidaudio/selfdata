with _src_users as (
  select * from {{ source('tap_lastfm', 'users') }}
  -- don't query all the back partitions since we only care about the most recent data
  where dt >= (select max(dt) from {{ source('tap_lastfm', 'users') }})
),

_ref_user_timezones as (
  select * from {{ ref('lastfm_user_timezones') }}
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
  from _src_users u
  left join _ref_user_timezones ut on ut.username = u.username
)

select * from lastfm_users
