# Greek Nouns List
| ID | Gender | Word | Translation | Comment |
|----|--------|------|------------|---------|
{% for noun in tables.nouns %}| {{ noun.id }} | {{ noun.gender or '' }} | `{{ noun.word or '' }}` | {{ noun.translation or '' }} | {{ noun.comment or '' }} |
{% endfor %}

*You can also edit this Markdown manually after generation.*
