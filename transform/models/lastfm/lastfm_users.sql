with _src_users as (
  select * from {{ source('tap_lastfm', 'users') }}
),

lastfm_users as (
  SELECT
    username,
    realname as name,
    url,
    country,
    age,
    gender,
    subscriber as is_subscriber,
    {{ eastern_time('registered_at') }} as registered_at
  FROM _src_users
)

select * from lastfm_users
