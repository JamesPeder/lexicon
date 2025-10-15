{% macro render_table(data, attributes) %}
{% if data and attributes %}
| {% for attr in attributes %}{{ attr }}{% if not loop.last %} | {% endif %}{% endfor %} |
| {% for attr in attributes %}-----{% if not loop.last %} | {% endif %}{% endfor %} |
{% for row in data -%}
| {% for attr in attributes -%}
    {{ row[attr] if row[attr] is not none else '' }}{% if not loop.last %} | {% endif %}
{%- endfor %} |
{% endfor %}
{% else %}
_No data available._
{% endif %}
{% endmacro %}

{% macro join_strings(strings) -%}
    {%- set parts = [] -%}
    {%- for s in strings -%}
        {%- set val = s | default('') | trim -%}
        {%- if val != '' -%}
            {%- set _ = parts.append(val) -%}
        {%- endif -%}
    {%- endfor -%}
    {{ parts | join(', ') }}
{%- endmacro %}

{% macro wrap_string(value, char) -%}
    {{ char ~ value ~ char }}
{%- endmacro %}

{% macro italics(value) -%}
    {{ wrap_string(value, '*') }}
{%- endmacro %}

{% macro bold(value) -%}
    {{ wrap_string(value, '**') }}
{%- endmacro %}

{% macro highlighted(value) -%}
    {{ wrap_string(value, '`') }}
{%- endmacro %}

