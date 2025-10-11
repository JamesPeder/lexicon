
# Greek


##  Adverbs / Adjectives

| Greek | Translation | Comment |
|-------|-------------|---------|
{% for adverb_adjective in tables.adverbs_adjectives %}| `{{ adverb_adjective.adjective_male }}` | *{{ adverb_adjective.translation }}* | {{ adverb_adjective.comment }} |
{% endfor %}


## Verbs

| Greek | Translation | Comment |
|-------|-------------|---------|
{% for verb in tables.verbs %}| `{{ verb.word }}` | *{{ verb.translation }}* | {{ verb.comment }} |
{% endfor %}


## Nouns

| Article | Greek | Translation | Comment |
|---------|-------|-------------|---------|
{% for noun in tables.nouns %}| *{{ noun.gender }}* | `{{ noun.word }}` | *{{ noun.translation }}* | {{ noun.comment }} |
{% endfor %}

## Preposition

`πάνω` - *on*

Εxample: *Το παιδί είναι πάνω σε ένα ξύλινο άλογο*

`Πίσω` - *behind*


## Numbers

| Greek | Number | Ordinal | Comment |
|-------|--------|---------|---------|
{% for number in tables.numbers %}| `{{ number.word }}` | *{{ number.number }}* | {{ number.ordinal }} | {{ number.comment }} |
{% endfor %}

