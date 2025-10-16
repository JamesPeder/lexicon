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
