from src import gathering
import yaml


with open('src/config.yml') as file:
    data = yaml.safe_load(file)

gat = gathering.DataGather()



# esempio semopenalex

semopenalex = gat.semopenalex(data['sparql']['semopenalex'])


# ci sono solo alcuni esempi delle api di semantic scholar per cercare. guarda le ref qui: https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search

sem_search = 'a' #gat.scholar_search_author(data['queries']['author_scholar'],data['apis']['semantic_scholar'])


# ci sono solo alcuni esempi delle api di semantic scholar per recuperare informazioni dagli id. guarda le ref qui: https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_paper_bulk_search


sem_retrieve = 'a' #gat.bulk_papers_retrieval(data['queries']['paper_ids'],data['apis']['semantic_scholar'],data['fields']['paper_info'])



cordis = gat.cordis(data['sparql']['cordis'])

print(cordis)