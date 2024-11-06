import requests


QUERY = '''
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
  ?author foaf:name "Rossana Damiano"^^xsd:string .
  ?author org:memberOf ?institution .
  ?paper dcterms:title ?paperTitle.
  ?paper fabio:hasPublicationYear ?pubblicationYear .
  ?work soa:hasKeyword ?keyword.
  #?work dcterms:abstract ?abstract.
  ?author dbpedia-owl:orcidId ?orcidID
 
}
'''

CORDIS_QUERY = '''
PREFIX eurio:<http://data.europa.eu/s66#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?project ?start ?end ?proLab ?xLab ?person
WHERE
{
  ?project eurio:isFundedBy ?grant; rdfs:label ?proLab .
  
  ?grant eurio:hasBeneficiary ?x ; eurio:startDate ?start ; eurio:endDate ?end.
  ?x rdfs:label ?xLab; eurio:isRoleOf ?org .
  ?org rdfs:label ?orgLab .
  
  FILTER(regex(?xLab,'universita degli studi di torino','i')).
} ORDER BY DESC(?end)

'''
URL = 'https://semopenalex.org/sparql' 
API = "my_key"


class DataGather:

    def __init__(self):

        URL = 'https://semopenalex.org/sparql'



    def semopenalex(self,query=QUERY,url=URL,headers={"Accept": "application/sparql-results+json"}):
        
        params = {'query':query,'format':'json'}

        req = requests.get(url,params=params,headers=headers)
        return req.json()
    
    def scholar_search_author(self,query='viviana patti',url="https://api.semanticscholar.org/graph/v1/author/search",api=API):
        
        params = {'query':query}
        headers = {'X-API-KEY':api}
        req = requests.get(url,params=params,headers=headers)

        return req.json()
    
    def scholar_search_paper(self,query='WikiBio: a semantic resource for the intersectional analysis of biographical events',url="https://api.semanticscholar.org/graph/v1/paper/search/match",api=API):
        
        params = {'query':query}
        headers = {'X-API-KEY':api}
        req = requests.get(url,params=params,headers=headers)

        return req.json()
    
    def bulk_papers_retrieval(self,url='https://api.semanticscholar.org/graph/v1/paper/batch',api=API,ids=['0f9d73aff3db64622c9a4d1a146f79ef1b8e5c70'],fields='title,authors,citations.title,citations.abstract'):
        params = {'fields':'title,authors,citations.title,citations.abstract'}
        all_ids = {'ids':ids}
        print(all_ids)

        #req = requests.post(url,params,json=all_ids)
        req = requests.post(
    'https://api.semanticscholar.org/graph/v1/paper/batch',
    params={'fields': 'title,authors,abstract,citations.title,citations.abstract,references.title,references.abstract'},
    json={"ids": ids}
)

        return req.json()
    

    def cordis(self,url='https://cordis.europa.eu/datalab/sparql-endpoint/endatalab/sparql',query=CORDIS_QUERY):
        params = {'query':query,'format':'json'}
        headers = {"Accept": "application/sparql-results+json"}

        req = requests.post(url,params=params,headers=headers)
        print(req.text)
        return req.json()




gat = DataGather()

print(gat.cordis())