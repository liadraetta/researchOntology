from src import gathering
import yaml
import requests
import json
from src import helper


with open('src/config.yml') as file:
    data = yaml.safe_load(file)

gat = gathering.DataGather()



# esempio semopenalex

#semopenalex = gat.semopenalex(data['sparql']['semopenalex'])


# ci sono solo alcuni esempi delle api di semantic scholar per cercare. guarda le ref qui: https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search

sem_search = gat.scholar_search_author(data['queries']['author_scholar'],data['apis']['semantic_scholar'])


# ci sono solo alcuni esempi delle api di semantic scholar per recuperare informazioni dagli id. guarda le ref qui: https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search

#sem_retrieve = 'a' #gat.bulk_papers_retrieval(data['queries']['paper_ids'],data['apis']['semantic_scholar'],data['fields']['paper_info'])

# retrieve author from author_id and author paper information
#bulk_author_search = gat.scholar_search_author_bulk(data['queries']['author_ids'],data['apis']['semantic_scholar'],data['fields']['author_info'])

#paper_bulk = gat.bulk_papers_retrieval_new(data['queries']['query'],data['apis']['semantic_scholar'],data['fields']['paper_info'])


#cordis = gat.cordis(data['sparql']['cordis'])
#response = paper_bulk
#print(bulk_author_search)

iris_full_names = {" ".join(author["column"]).lower() for author in helper.iris_authors}

# IRIS NAME matching
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


def fetch_author_details(response, batch_size=10, output_file="authors_output_prova.json"):
    author_ids = []  #
    for item in response:
        print('item', item)
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



fetch_author_details(get_author_ids(helper.iris_authors_1))