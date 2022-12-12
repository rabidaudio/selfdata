
{% macro most_recent_version(src_table, partition_key = 'dt') %}
  select * from {{ src_table }}
  -- don't query all the back partitions since we only care about the most recent data
  where {{ partition_key }} >= (select max({{ partition_key }}) from {{ src_table }})
{% endmacro %}

-- When using partitions in S3, there's no record deduplication if the
-- same data is fetched multiple times.
-- To avoid this, we have to select the most recent version of each
-- record.
{% macro distinct_on(src_table, primary_keys, sort_key = '_sdc_sequence') %}
    select a.*
    from {{ src_table }} a
    inner join (
        select {{ primary_keys | join(', ') }}, max({{ sort_key }}) as {{ sort_key }}
        from {{ src_table }}
        group by {{ primary_keys | join(', ') }}
    ) b on 
        {% for primary_key in primary_keys %}
            b.{{ primary_key }} = a.{{ primary_key }}
            {% if not loop.last %} and {% endif %}
        {% endfor %}
        and b.{{ sort_key }} = a.{{ sort_key }}
{% endmacro %}
