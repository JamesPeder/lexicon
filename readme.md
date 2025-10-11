# Greek Notebook

Welcome to the Greek notebook.

This app runs on python flask. Run the main.py to start.
A sqllite database will be created. You can also edit the sql script to match the fields you would like to include for your database.
You can add words and phrases to the database over the manage endpoint `http://127.0.0.1:5000/manage`, which acts as a datbase management GUI.

The APIs to update the Database are kept general, so there should be no issues with custom tables etc. Only some minor enum tweaks would be necessary.

Every time a word is added, edited or deleted, the markdown file is updated. This file contains words that you have marked as the most difficult for you to remember. Once you get used to these words, you can decrease the perceived difficulty of a word, meaning other words will be shownw to you over the markdown file.

You can also edit the markdown.md file template to include other notes, or include data from the database tables in additional ways, than already included. This project uses the jinja templating language, so is easily extensible for note taking etc. The data is included in the preview.md file, once a render is triggered by the API or over the management GUI.  


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