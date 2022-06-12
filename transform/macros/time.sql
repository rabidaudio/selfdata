{%- macro eastern_time(column) -%}
  timezone('US/Eastern', {{ column }}::timestamptz)
{%- endmacro -%}
