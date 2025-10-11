#!/bin/bash

URL="http://127.0.0.1:5000/word"
HEADER="Content-Type: application/json"

# Define Greek numbers → (number, ordinal)
declare -A numbers
numbers["Τέσσερα"]="4|τέταρτος"
numbers["δέκα"]="10|"
numbers["δεκαέξι"]="16|"
numbers["δεκαοκτώ"]="18|"
numbers["τριάντα"]="30|"

for word in "${!numbers[@]}"; do
  IFS='|' read -r number ordinal <<< "${numbers[$word]}"
  echo "🟢 Inserting number: $word → $number (${ordinal:-no ordinal})"

  curl -s -X POST "$URL" \
    -H "$HEADER" \
    -d "{
      \"table\": \"numbers\",
      \"key\": \"number\",
      \"data\": {
        \"word\": \"$word\",
        \"number\": $number,
        \"ordinal\": \"$ordinal\"
      }
    }" | jq '.'

  echo
done

echo "✅ All numbers inserted successfully!"
