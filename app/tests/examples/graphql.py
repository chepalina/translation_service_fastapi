import requests


query = """
query GetWords($page: Int, $pageSize: Int, $wordFilter: String, $includeDefinitions: Boolean, 
$includeSynonyms: Boolean, $includeTranslations: Boolean, $includeExamples: Boolean) {
  words(
    page: $page, 
    pageSize: $pageSize, 
    wordFilter: $wordFilter, 
    includeDefinitions: $includeDefinitions, 
    includeSynonyms: $includeSynonyms, 
    includeTranslations: $includeTranslations, 
    includeExamples: $includeExamples
  ) {
    word
    language
    definitions {
      definition
    }
    synonyms {
      synonym
    }
    translations {
      translation
    }
    examples {
      example
    }
  }
}
"""

variables = {
    "page": 1,
    "pageSize": 10,
    "wordFilter": "a",
    "includeDefinitions": True,
    "includeSynonyms": True,
    "includeTranslations": True,
    "includeExamples": True,
}


url = "http://localhost:8000/api/v1/graphql"  # Replace with your GraphQL endpoint

response = requests.post(url, json={"query": query, "variables": variables})

if response.status_code == 200:
    print(response.json())
else:
    print(
        "Query failed to run with a status code of {}. {}".format(
            response.status_code, query
        )
    )
