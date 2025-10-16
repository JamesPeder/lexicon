{%- import "resources/macros.md" as macros -%}
# Greek
{%- set max_rows_to_show = 10 -%}
{%- set max_examples_to_show = 3 %}


## Adverbs / Adjectives
{%- set sorted_adverb_adjectives = (tables.adverbs_adjectives | default_sort)[:max_rows_to_show] -%}
{%- set processed_adverb_adjectives = [] -%}
{%- for adverb_adjective in sorted_adverb_adjectives -%}
    {%- 
    set greek = macros.join_strings([
        adverb_adjective.adjective_male,
        adverb_adjective.adjective_female,
        adverb_adjective.adjective_neutral,
        adverb_adjective.adverb
    ]) -%}
    {%- 
    set _ = processed_adverb_adjectives.append({
        'Greek': macros.highlighted(greek),
        'Translation': macros.italics(adverb_adjective.translation),
        'Comment': adverb_adjective.comment
    }) -%}
{%- endfor -%}

{{ macros.render_table(processed_adverb_adjectives, ['Greek', 'Translation', 'Comment']) -}}
{{ macros.render_examples("adverbs_adjectives", sorted_adverb_adjectives, examples, max_examples_to_show) }}


## Verbs
{%- set sorted_verbs = (tables.verbs | default_sort)[:max_rows_to_show] -%}
{%- set processed_verbs = [] -%}
{%- for verb in sorted_verbs -%}
    {%- 
    set _ = processed_verbs.append({
        'Greek': macros.highlighted(verb.word),
        'Translation': macros.italics(verb.translation),
        'Comment': verb.comment
    }) -%}
{%- endfor -%}

{{ macros.render_table(processed_verbs, ['Greek', 'Translation', 'Comment']) -}}
{{ macros.render_examples("verbs", sorted_verbs, examples, max_examples_to_show) }}


## Nouns
{%- set sorted_nouns = (tables.nouns | default_sort)[:max_rows_to_show] -%}
{%- set processed_nouns = [] -%}
{%- for noun in sorted_nouns -%}
    {% 
    set _ = processed_nouns.append({
        'Article': macros.italics(noun.gender),
        'Greek': macros.highlighted(noun.word),
        'Translation': macros.italics(noun.translation),
        'Comment': noun.comment
    }) -%}
{%- endfor -%}

{{ macros.render_table(processed_nouns, ['Article', 'Greek', 'Translation', 'Comment']) -}}
{{ macros.render_examples("nouns", sorted_nouns, examples, max_examples_to_show) }}


## Prepositions
{%- set sorted_prepositions = (tables.prepositions| default_sort)[:max_rows_to_show] %}
{% for preposition in sorted_prepositions %}

`{{ preposition.word }}` - *{{ preposition.translation }}*
{%- if preposition.comment -%}
    *{{ preposition.comment }}*
{%-  endif -%}

{{ macros.render_examples("prepositions", [preposition], examples, max_examples_to_show, "") }}
{% endfor %}

## Numbers
{%- set sorted_numbers = (tables.numbers | default_sort)[:max_rows_to_show] -%}
{%- set processed_numbers = [] -%}
{%- for number in sorted_numbers -%}
    {%- 
    set _ = processed_numbers.append({
        'Greek': macros.highlighted(number.word),
        'Number': macros.italics(number.number),
        'Ordinal': number.ordinal,
        'Comment': number.comment
    }) -%}
{%- endfor -%}
{{ macros.render_table(processed_numbers, ['Greek', 'Number', 'Ordinal', 'Comment']) -}}
{{ macros.render_examples("numbers", sorted_numbers, examples, max_examples_to_show) }}

