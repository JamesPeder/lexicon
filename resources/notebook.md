
# Greek

{% set max_rows_to_show = 10 %}
{% set max_examples_to_show = 2 %}

##  Adverbs / Adjectives

| Greek | Translation | Comment |
|-------|-------------|---------|
{% for adverb_adjective in (
    tables.adverbs_adjectives 
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] 
%}| `{{ adverb_adjective.adjective_male }}` | *{{ adverb_adjective.translation }}* | {{ adverb_adjective.comment }} |
{% endfor %}


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
    )[:max_rows_to_show] %}`{{ preposition.word }}` - *{{ preposition.translation }}*{% if preposition_examples %}
{{ preposition.comment }}
{% endif %}{% set preposition_examples = examples.get(('prepositions', preposition.id)) %}{% if preposition_examples %}{% for preposition_examples in (
    preposition_examples
    | sort(attribute='created_at', reverse=True)
    )[:max_examples_to_show] %}
- {{ preposition_examples.example_text }}
{% endfor %}{% endif %}
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

