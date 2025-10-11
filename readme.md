# Greek Notebook

Welcome to the Greek notebook.

To add words, run the python server and execute these requests:

### Nouns
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "nouns",
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
  "table": "nouns",
  "data": {
    "gender": "το",
    "word": "κρεμμύδι",
    "translation": "onion"
  }                         
}'
```

### Verbs
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "nouns",
  "data": {
    "gender": "το",
    "word": "κρεμμύδι",
    "translation": "onion"
  }                         
}'
```

### Numbers
```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "nouns",
  "data": {
    "gender": "το",
    "word": "κρεμμύδι",
    "translation": "onion"
  }                         
}'
```


```
curl -X POST http://127.0.0.1:5000/word -H "Content-Type: application/json" -d '{
  "table": "nouns",
  "key": "word"
  "data": {
    "gender": "το",
    "word": "κρεμμύδι",
    "translation": "oniones"
  }                         
}'
```