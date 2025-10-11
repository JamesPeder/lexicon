# Greek Notebook

Welcome to the Greek notebook.

## Rerendering the notebook preview

```
curl -X POST http://127.0.0.1:5000/render
```

## Reading from the Database

```
curl "http://127.0.0.1:5000/words?table=nouns"
```

## Upserting

### Nouns
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "nouns",
  "key": "word",
  "data": {
    "gender": "το",
    "word": "κρεμμύδι",
    "translation": "onion"
  }                         
}'
```

### Adjectives / Adverbs
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "adverbs_adjectives",
  "key": "adjective_male",
  "data": {
    "adjective_male": "κρεμμύδι",
    "adjective_female": "κρεμμύδι",
    "adjective_neutral": "κρεμμύδι",
    "adverb": "κρεμμύδι",
    "translation": "onion"
  }                         
}'
```

### Verbs
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "verbs",
  "key": "word",
  "data": {
    "word": "κανω",
    "translation": "to do"
  }                         
}'
```

### Numbers
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "numbers",
  "key": "number",
  "data": {
    "word": "ένα",
    "number": 1,
    "ordinal": "πρωτως"
  }                         
}'
```

### Prepositions
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "prepositions",
  "key": "word",
  "data": {
    "word": "πάνω",
    "translation": "on"
  }                         
}'
```

### Examples
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "examples",
  "data": {
    "table_name": "prepositions",
    "word_id": 1,
    "example_text": "Το παιδί είναι πάνω σε ένα ξύλινο άλογο"
  }                         
}'
```


## Deleting

```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "nouns",
  "key": "word",
  "action": "delete",
  "data": {
    "gender": "το",
    "word": "κρεμμύδι",
    "translation": "oniones"
  }                         
}'
```