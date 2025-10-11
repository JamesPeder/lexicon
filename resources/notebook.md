
# Greek

{% set max_rows_to_show = 10 %}

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

`πάνω` - *on*

Εxample: *Το παιδί είναι πάνω σε ένα ξύλινο άλογο*

`Πίσω` - *behind*


## Numbers

| Greek | Number | Ordinal | Comment |
|-------|--------|---------|---------|
{% for number in (
    tables.numbers
    | sort(attribute='created_at', reverse=True)
    | sort(attribute='difficulty', reverse=True)
    )[:max_rows_to_show] %}| `{{ number.word }}` | *{{ number.number }}* | {{ number.ordinal }} | {{ number.comment }} |
{% endfor %}

