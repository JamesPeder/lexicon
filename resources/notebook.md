
# Greek

{% set max_rows_to_show = 10 %}
{% set max_examples_to_show = 3 %}

##  Adverbs / Adjectives
{% 
set sorted_adverb_adjectives = tables.adverbs_adjectives 
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
 %}
| Greek | Translation | Comment |
|-------|-------------|---------|
{% for adverb_adjective in sorted_adverb_adjectives[:max_rows_to_show] 
%}| `{{ adverb_adjective.adjective_male }}` | *{{ adverb_adjective.translation }}* | {{ adverb_adjective.comment }} |
{% endfor %}

{% set var = namespace(examples_count=0) %}

{% for adverb_adjective in sorted_adverb_adjectives %}
    {% set adverb_examples = examples.get(('adverbs_adjectives', adverb_adjective.id)) %}
    {% if adverb_examples %}
        {% for adverb_example in adverb_examples | sort(attribute='created_at', reverse=True) %}
            {% if var.examples_count < max_examples_to_show %}
                {% set var.examples_count = var.examples_count + 1 %}
            {% endif %}
        {% endfor %}
    {% endif %}
{% endfor %}

{% if var.examples_count > 0 %}
## Examples:

{% set var = namespace(examples_count=0) %}

{% for adverb_adjective in sorted_adverb_adjectives %}
{% set adverb_examples = examples.get(('adverbs_adjectives', adverb_adjective.id)) %}
{% if adverb_examples %}
{% for adverb_example in (adverb_examples | sort(attribute='created_at', reverse=True)) %}
{% if var.examples_count < max_examples_to_show %}
- `{{ adverb_example.example_text }}`{% if adverb_example.translation %}

    *{{ adverb_example.translation }}*{% endif %}{% if adverb_example.comment %} - {{ adverb_example.comment }}
{% endif %}{% set var.examples_count = var.examples_count + 1 %}
{% endif %}{% endfor %}
{% endif %}
{% endfor %}
{% endif %}


## Verbs

| Greek | Translation | Comment |
|-------|-------------|---------|
{% for verb in (
    tables.verbs
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] %}| `{{ verb.word }}` | *{{ verb.translation }}* | {{ verb.comment }} |
{% endfor %}


## Nouns

| Article | Greek | Translation | Comment |
|---------|-------|-------------|---------|
{% for noun in (
    tables.nouns
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] %}| *{{ noun.gender }}* | `{{ noun.word }}` | *{{ noun.translation }}* | {{ noun.comment }} |
{% endfor %}

## Preposition

{% for preposition in (
    tables.prepositions
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] %}
`{{ preposition.word }}` - *{{ preposition.translation }}*{% if preposition.comment %}
    
*{{ preposition.comment }}*
{% endif %}
{% set preposition_examples = examples.get(('prepositions', preposition.id)) %}{% if preposition_examples %}{% for preposition_example in (
    preposition_examples
    | sort(attribute='created_at', reverse=True)
    )[:max_examples_to_show] %}
- `{{ preposition_example.example_text }}`{% if preposition_example.translation %}
    
    *{{ preposition_example.translation }}*{% endif %}{% if preposition_example.comment %} - {{ preposition_example.comment }}
{% endif %}{% endfor %}{% endif %}
{% endfor %}

## Numbers

| Greek | Number | Ordinal | Comment |
|-------|--------|---------|---------|
{% for number in (
    tables.numbers
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] %}| `{{ number.word }}` | *{{ number.number }}* | {{ number.ordinal }} | {{ number.comment }} |
{% endfor %}

