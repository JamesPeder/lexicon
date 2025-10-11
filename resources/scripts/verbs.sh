#!/bin/bash

URL="http://127.0.0.1:5000/word"
HEADER="Content-Type: application/json"

# Define verbs → (translation|comment)
declare -A verbs
verbs["Χάρηκα"]="Nice to meet you|Aorist tense - I got pleased. I was gladdened"
verbs["χαίρομαι"]="to be glad or to rejoice|"
verbs["κάνω"]="to do|"

for word in "${!verbs[@]}"; do
  IFS='|' read -r translation comment <<< "${verbs[$word]}"
  echo "🟢 Inserting verb: $word → $translation"

  curl -s -X POST "$URL" \
    -H "$HEADER" \
    -d "{
      \"table\": \"verbs\",
      \"key\": \"word\",
      \"data\": {
        \"word\": \"$word\",
        \"translation\": \"$translation\",
        \"comment\": \"$comment\"
      }
    }" | jq '.'

  echo
done

echo "✅ All verbs inserted successfully!"
