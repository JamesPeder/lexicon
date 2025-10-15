{% import "resources/macros.md" as macros %}
# Greek
{% 
set max_rows_to_show = 10 %}{% 
set max_examples_to_show = 3 
%}

## Adverbs / Adjectives
{% set sorted_adverb_adjectives = (
    tables.adverbs_adjectives
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
)[:max_rows_to_show] -%}{% 
set processed_adverb_adjectives = [] -%}{% 
for adverb_adjective in sorted_adverb_adjectives -%}
    {% set greek = macros.join_strings([
    adverb_adjective.adjective_male,
    adverb_adjective.adjective_female,
    adverb_adjective.adjective_neutral,
    adverb_adjective.adverb
]) %}{% 
    set _ = processed_adverb_adjectives.append({
        'Greek': macros.highlighted(greek),
        'Translation': macros.italics(adverb_adjective.translation),
        'Comment': adverb_adjective.comment
    }) -%}{% 
endfor -%}

{{ macros.render_table(processed_adverb_adjectives, ['Greek', 'Translation', 'Comment']) -}}
{{ macros.render_examples("adverbs_adjectives", sorted_adverb_adjectives, examples, max_examples_to_show) }}


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
{{ macros.render_example(example) }}
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
{{ macros.render_example(example) }}
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
{{          macros.render_example(preposition_example) }}{% 
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
{{ macros.render_example(example) }}
{%              set var.examples_count = var.examples_count + 1 %}{% 
            endif %}{% 
        endfor %}{% 
    endif %}{% 
endfor %}

