#!/bin/bash

URL="http://127.0.0.1:5000/word"
HEADER="Content-Type: application/json"

# Nouns: Greek word → Translation
declare -A nouns=(
  ["σπαγγέτι"]="spaghetti"
  ["σκόρδο"]="garlic"
  ["κρεμμύδι"]="onion"
  ["καιρός"]="weather"
)

GENDER="το"

for word in "${!nouns[@]}"; do
  translation=${nouns[$word]}
  echo "🟢 Inserting noun: $GENDER $word → $translation"

  curl -s -X POST "$URL" \
    -H "$HEADER" \
    -d "{
      \"table\": \"nouns\",
      \"key\": \"word\",
      \"data\": {
        \"gender\": \"$GENDER\",
        \"word\": \"$word\",
        \"translation\": \"$translation\"
      }
    }" \
  | jq '.'  # Optional: Pretty-print JSON response

  echo
done

echo "✅ All nouns inserted successfully!"
