#!/bin/bash

# Prepositions to add
declare -A prepositions=(
  ["πάνω"]="on"
  ["Πίσω"]="behind"
)

for word in "${!prepositions[@]}"; do
  translation=${prepositions[$word]}
  echo "Adding preposition: $word -> $translation"

  curl -s -X POST http://127.0.0.1:5000/word \
       -H "Content-Type: application/json" \
       -d "{
            \"table\": \"prepositions\",
            \"key\": \"word\",
            \"data\": {
                \"word\": \"$word\",
                \"translation\": \"$translation\"
            }
       }"
  echo -e "\n"
done
