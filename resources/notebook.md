{% import "resources/macros.md" as macros %}
# Greek
{% 
set max_rows_to_show = 10 %}{% 
set max_examples_to_show = 3 
%}{% 

macro render_example(example) -%}
- `{{ example.example_text }}`
    {% if example.translation %}    
    *{{ example.translation }}*{% endif %}{% if example.comment %} - {{ example.comment }}{% 
    endif %}{%- 
endmacro %}

## Adverbs / Adjectives
{% set sorted_adverb_adjectives = (
    tables.adverbs_adjectives
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
)[:max_rows_to_show] -%}
{% set processed = [] -%}
{% for adverb_adjective in sorted_adverb_adjectives -%}
    {% set parts = [
        adverb_adjective.adjective_male,
        adverb_adjective.adjective_female,
        adverb_adjective.adjective_neutral,
        adverb_adjective.adverb
    ]
    | map('default', '')
    | map('trim')
    | reject('equalto', '')
    | join(', ') -%}

    {% set _ = processed.append({
        'Greek': parts,
        'Translation': '*' ~ adverb_adjective.translation ~ '*',
        'Comment': adverb_adjective.comment
    }) -%}
{% endfor -%}

{{ macros.render_table(processed, ['Greek', 'Translation', 'Comment']) -}}
{% 

set var = namespace(examples_count=0) 
%}{% 
for adverb_adjective in sorted_adverb_adjectives %}{% 
    set adverb_examples = examples.get(('adverbs_adjectives', adverb_adjective.id)) %}{% 
    if adverb_examples %}{% 
        for example in adverb_examples | sort(attribute='created_at', reverse=True) %}{% 
            if var.examples_count < max_examples_to_show %}{% 
                if var.examples_count == 0 %}
### Examples:
{%              endif %}
{{ render_example(example) }}
{%              set var.examples_count = var.examples_count + 1 %}{% 
            endif %}{% 
        endfor %}{% 
    endif %}{% 
endfor %}


## Verbs
{% set sorted_verbs = (
    tables.verbs
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] 
%}
| Greek | Translation | Comment |
|-------|-------------|---------|
{% for verb in sorted_verbs %}| `{{ verb.word }}` | *{{ verb.translation }}* | {{ verb.comment }} |
{% endfor %}{%

set var = namespace(examples_count=0) 
%}{% 
for verb in sorted_verbs %}{% 
    set verb_examples = examples.get(('verbs', verb.id)) %}{% 
    if verb_examples %}{% 
        for example in verb_examples | sort(attribute='created_at', reverse=True) %}{% 
            if var.examples_count < max_examples_to_show %}{% 
                if var.examples_count == 0 %}
### Examples:
{%              endif %}
{{ render_example(example) }}
{%              set var.examples_count = var.examples_count + 1 %}{% 
            endif %}{% 
        endfor %}{% 
    endif %}{% 
endfor %}


## Nouns
{% set sorted_nouns = (
    tables.nouns
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] 
%}
| Article | Greek | Translation | Comment |
|---------|-------|-------------|---------|
{% for noun in sorted_nouns %}| *{{ noun.gender }}* | `{{ noun.word }}` | *{{ noun.translation }}* | {{ noun.comment }} |
{% endfor %}{%

set var = namespace(examples_count=0) 
%}{% 
for noun in sorted_nouns %}{% 
    set noun_examples = examples.get(('nouns', noun.id)) %}{% 
    if noun_examples %}{% 
        for example in noun_examples | sort(attribute='created_at', reverse=True) %}{% 
            if var.examples_count < max_examples_to_show %}{% 
                if var.examples_count == 0 %}
### Examples:
{%              endif %}
{{ render_example(example) }}
{%              set var.examples_count = var.examples_count + 1 %}{% 
            endif %}{% 
        endfor %}{% 
    endif %}{% 
endfor %}

## Prepositions

{% for preposition in (
    tables.prepositions
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] %}
`{{ preposition.word }}` - *{{ preposition.translation }}*
{% 
    if preposition.comment %}
*{{ preposition.comment }}*
{%  endif %}
{% set preposition_examples = examples.get(('prepositions', preposition.id)) %}{% 
    if preposition_examples %}{% 
        for preposition_example in (
            preposition_examples
            | sort(attribute='created_at', reverse=True)
        )[:max_examples_to_show] %}
{{          render_example(preposition_example) }}{% 
        endfor %}{% 
    endif %}
{% endfor %}

## Numbers
{% set sorted_numbers = (
    tables.numbers
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] 
%}
| Greek | Number | Ordinal | Comment |
|-------|--------|---------|---------|
{% for number in sorted_numbers %}| `{{ number.word }}` | *{{ number.number }}* | {{ number.ordinal }} | {{ number.comment }} |
{% endfor %}{%

set var = namespace(examples_count=0) 
%}{% 
for number in sorted_numbers %}{% 
    set number_examples = examples.get(('numbers', number.id)) %}{% 
    if number_examples %}{% 
        for example in number_examples | sort(attribute='created_at', reverse=True) %}{% 
            if var.examples_count < max_examples_to_show %}{% 
                if var.examples_count == 0 %}
### Examples:
{%              endif %}
{{ render_example(example) }}
{%              set var.examples_count = var.examples_count + 1 %}{% 
            endif %}{% 
        endfor %}{% 
    endif %}{% 
endfor %}

