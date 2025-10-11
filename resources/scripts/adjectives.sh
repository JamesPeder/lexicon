#!/bin/bash

URL="http://127.0.0.1:5000/word"
HEADER="Content-Type: application/json"

declare -A words=(
  ["Πιθανό"]="possible"
  ["εξαιρετικό"]="excellent"
  ["επίσημα"]="formal"
  ["νόμιμο"]="legal"
  ["σημαντικό"]="important"
  ["κλειστό"]="closed"
  ["ανοιχτό"]="open"
  ["φυσιολογικό"]="normal"
  ["ζωντανό"]="living, alive"
  ["διάσημος"]="famous"
  ["τέλειο"]="perfect"
  ["τελικός"]="final"
  ["κουρασμένο"]="tired"
  ["δίγλωσσο"]="bilingual"
  ["βασικός"]="basic"
  ["απαραίτητο"]="necessary"
  ["άσχημος"]="ugly, unattractive, bad, unpleasant"
  ["όμορφος"]="beautiful"
  ["στρατιωτικός"]="military, soldier"
  ["νέος"]="young, new"
  ["τοπικός"]="local"
  ["επόμενος"]="next"
  ["ολόκληρο"]="whole"
)

for greek in "${!words[@]}"; do
  translation=${words[$greek]}
  echo "🟢 Inserting: $greek → $translation"

  curl -s -X POST "$URL" \
    -H "$HEADER" \
    -d "{
      \"table\": \"adverbs_adjectives\",
      \"key\": \"adjective_male\",
      \"data\": {
        \"adjective_male\": \"$greek\",
        \"translation\": \"$translation\"
      }
    }" \
  | jq '.'  # Optional: formats JSON output (requires jq)

  echo
done

echo "✅ All adjectives/adverbs inserted successfully!"
