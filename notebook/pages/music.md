# Music Scrobbles

```users
select username, url from lastfm_users
```

<ul>
{#each users as user}
  <li><a href={user.url}><Value data={user} column=username/></a></li>
{/each}
</ul>

```listens_per_year
select username, cast(strftime('%Y', month) as int) as year, sum(listens) as listens
from listens_per_month
group by username, year
order by year, username
```

<LineChart 
    data={listens_per_year} 
    x=year 
    y=listens 
    series=username
    handleMissing=zero
/>
