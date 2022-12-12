with scrobbles as (
    select * from {{ ref('scrobbles') }}
),

scrobbles_with_month as (
    select date_trunc('month', scrobbled_at) as month, username
    from scrobbles
)
select month, username, count(1) as listens
from scrobbles_with_month
group by month, username
order by month, username
