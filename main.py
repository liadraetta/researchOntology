from src import gathering
import yaml
import requests
import json
from src import helper


with open('src/config.yml') as file:
    data = yaml.safe_load(file)

gat = gathering.DataGather()



# esempio semopenalex

semopenalex = gat.semopenalex(data['sparql']['semopenalex'])


# ci sono solo alcuni esempi delle api di semantic scholar per cercare. guarda le ref qui: https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search

sem_search = gat.scholar_search_author(data['queries']['author_scholar'],data['apis']['semantic_scholar'])


# ci sono solo alcuni esempi delle api di semantic scholar per recuperare informazioni dagli id. guarda le ref qui: https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search

#sem_retrieve = 'a' #gat.bulk_papers_retrieval(data['queries']['paper_ids'],data['apis']['semantic_scholar'],data['fields']['paper_info'])

# retrieve author from author_id and author paper information
#bulk_author_search = gat.scholar_search_author_bulk(data['queries']['author_ids'],data['apis']['semantic_scholar'],data['fields']['author_info'])

#paper_bulk = gat.bulk_papers_retrieval_new(data['queries']['query'],data['apis']['semantic_scholar'],data['fields']['paper_info'])


#cordis = gat.cordis(data['sparql']['cordis'])
#response = paper_bulk

#print(semopenalex)

def save_output(api_call, output_file="api_output.json"):
    response = api_call
    with open(output_file, "w") as json_file:
        json.dump(response, json_file, indent=4)


iris_full_names = {" ".join(author["column"]).lower() for author in helper.iris_authors}

def name_matching(api_response):
    filtered_papers = []
    for paper in api_response['data']:
        authors = paper.get('authors', [])
        for author in authors:
            author_name = author['name'].lower()
            author_parts = author_name.split()
            if len(author_parts) > 1:
                normalized_name = f"{author_parts[0]} {author_parts[-1]}"
            else:
                normalized_name = author_parts[0]  # Single name case
            if normalized_name in iris_full_names:
                filtered_papers.append(paper)
                break
    print(filtered_papers)

#name_matching(response)


def get_author_ids(iris_authors):
    results = []
    for author in iris_authors:
        full_name = " ".join(author["column"])
        url = f"https://api.semanticscholar.org/graph/v1/author/search?query={full_name}"
        req = requests.get(url)
        response = req.json()
        results.append(response)
    return results


def fetch_author_details(response, batch_size=10, output_file="authors_output_dip_info.json"):
    author_ids = []  #
    for item in response:
        for author in item.get('data', []):
            author_ids.append(author.get('authorId'))
    batches = [author_ids[i:i + batch_size] for i in range(0, len(author_ids), batch_size)]
    all_details = []
    for batch in batches:
        url = 'https://api.semanticscholar.org/graph/v1/author/batch'
        payload = {"ids": batch}
        params = {
            'fields': 'externalIds,name,hIndex,citationCount,affiliations,papers,papers.title,papers.year,papers.openAccessPdf,papers.fieldsOfStudy,papers.journal'}
        try:
            r = requests.post(url, params=params, json=payload)
            details = r.json()
            all_details.extend(details)
        except Exception as e:
            print(f"error {batch}: {e}")

    with open(output_file, "w") as json_file:
        json.dump(all_details, json_file, indent=4)

    return all_details


fetch_author_details(get_author_ids(helper.iris_authors))

# RETRIEVE DATA FROM SEMOPENALEX SPARQL ENDPOINT

SPARQL_ENDPOINT = "https://semopenalex.org/sparql"

iris_authors = helper.iris_authors_1

SPARQL_TEMPLATE = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX soa: <https://semopenalex.org/ontology/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX fabio: <http://purl.org/spar/fabio/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX dbpedia-owl: <https://dbpedia.org/ontology/>

SELECT ?authorName ?paper ?paperTitle ?institution ?pubblicationYear ?keyword ?orcidID ?abstract WHERE {
  ?paper soa:hasAuthorship ?authorship .
  ?authorship soa:hasAuthor ?author .
  ?author foaf:name ?authorName .
  ?author org:memberOf ?institution .
  ?paper dcterms:title ?paperTitle.
  ?paper fabio:hasPublicationYear ?pubblicationYear .
  ?work soa:hasKeyword ?keyword.
  ?author dbpedia-owl:orcidId ?orcidID
  FILTER ({filter_conditions})
}

"""

def create_filter_conditions(authors):
    conditions = []
    for author in authors:
        full_name = " ".join(part.title() for part in author["column"])
        conditions.append(f'?authorName = "{full_name}"')
    return " || ".join(conditions)


def query_semopenalex(authors):
    filter_conditions = create_filter_conditions(authors)
    sparql_query = SPARQL_TEMPLATE.replace("{filter_conditions}", filter_conditions)
    response = requests.post(SPARQL_ENDPOINT, data={"query": sparql_query},
                             headers={"Accept": "application/sparql-results+json"})
    return response.json()

try:
    results = query_semopenalex(iris_authors)
except Exception as e:
    print(f"Error: {e}")


def save_output(api_call, output_file):
    response = api_call
    with open(output_file, "w") as json_file:
        json.dump(response, json_file, indent=4)

# Here to query the SemOpenAlex endpoint
#save_output(query_semopenalex(iris_authors), output_file="open_alex_output.json")