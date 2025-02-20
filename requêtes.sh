curl -X DELETE "http://localhost:9200/deputes"
curl -X GET "http://localhost:9200/deputes"

curl -X PUT "http://localhost:9200/deputes" -H "Content-Type: application/json" -d @mapping.json
curl -X GET "http://localhost:9200/deputes/_mapping?pretty=true"

jq '(.deputes[].depute.profession) |= tostring' deputes_synthese.json > deputes_synthese_clean.json
jq -c '.deputes[] | {"index": {"_index": "deputes"}}, .' deputes_synthese_clean.json > bulk_deputes.json

curl -X POST "http://localhost:9200/_bulk" -H "Content-Type: application/json" --data-binary "@bulk_deputes.json"
curl -X GET "http://localhost:9200/deputes/_search?pretty=true"






curl -X GET "http://localhost:9200/deputes/_search" -H "Content-Type: application/json" -d '
{
  "query": {
    "match": {
      "depute.profession": "agriculteur"
    }
  }
}'

curl -X GET "http://localhost:9200/deputes/_search" -H "Content-Type: application/json" -d '
{
  "size": 0,
  "aggs": {
    "professions_count": {
      "terms": {
        "field": "depute.profession.keyword",
        "size": 10
      }
    }
  }
}'

curl -X GET "http://localhost:9200/deputes/_search" -H "Content-Type: application/json" -d '
{
  "query": {
    "match": {
      "depute.nom": {
        "query": "macr",
        "analyzer": "edge_ngram"
      }
    }
  }
}'

curl -X GET "http://localhost:9200/deputes/_search" -H "Content-Type: application/json" -d '
{
  "query": {
    "fuzzy": {
      "depute.nom": {
        "value": "macorn",
        "fuzziness": 2
      }
    }
  }
}'

curl -X GET "http://localhost:9200/deputes/_search" -H "Content-Type: application/json" -d '
{
  "size": 0,
  "aggs": {
    "deputes_par_annee": {
      "date_histogram": {
        "field": "depute.mandat_debut",
        "calendar_interval": "year"
      }
    }
  }
}'


