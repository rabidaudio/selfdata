# Music Scrobbles

```users
select username, url from lastfm_users
```

{#each users as user}
  <h1><a href={user.url}><Value data={user} column=username/></a></h1>
{/each}

```listens_per_month
select date_trunc('month', scrobbled_at) as month, username, count(1) as listens
from scrobbles
group by month, username
order by month, username
```

<LineChart 
    data={listens_per_month} 
    x=month 
    y=listens 
    series=username 
/>