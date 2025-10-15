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

{% macro render_example(example) -%}
  
- `{{ example.example_text }}`
    {% if example.translation %}    
    *{{ example.translation }}*{% endif %}{% if example.comment %} - {{ example.comment }}{% endif %}
{%- endmacro %}

{% macro render_examples(table_name, data_list, example_mapping, max_examples=5, header="### Examples:") -%}
{%- set var = namespace(count=0) -%}

{%- for item in data_list -%}
    {%- set item_examples = example_mapping.get((table_name, item.id)) -%}
    {%- if item_examples -%}
        {%- for example in item_examples | sort(attribute='created_at', reverse=True) -%}
            {%- if var.count < max_examples -%}
                {% if var.count == 0 %}
{{ header }}{% endif %}
                
{{ render_example(example) }}
                {%- set var.count = var.count + 1 -%}
            {%- endif -%}
        {%- endfor -%}
    {%- endif -%}
{%- endfor -%}
{%- endmacro %}



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

