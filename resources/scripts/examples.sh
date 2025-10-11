#!/bin/bash

# Example entries to add
declare -A examples=(
  ["1"]="Το παιδί είναι πάνω σε ένα ξύλινο άλογο"
  ["2"]="Η γάτα κρύφτηκε πίσω από τον καναπέ"
)

for word_id in "${!examples[@]}"; do
  example_text=${examples[$word_id]}
  echo "Adding example for word_id $word_id: $example_text"

  curl -s -X POST http://127.0.0.1:5000/word \
       -H "Content-Type: application/json" \
       -d "{
            \"table\": \"examples\",
            \"data\": {
                \"table_name\": \"prepositions\",
                \"word_id\": $word_id,
                \"example_text\": \"$example_text\"
            }
       }"
  echo -e "\n"
done
