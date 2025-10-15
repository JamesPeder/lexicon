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
