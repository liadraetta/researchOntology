import requests


class DataGather:

    def __init__(self):

        pass



    def semopenalex(self,query,url='https://semopenalex.org/sparql',headers={"Accept": "application/sparql-results+json"}):
        
        params = {'query':query,'format':'json'}

        req = requests.get(url,params=params,headers=headers)
        return req.json()
    
    def scholar_search_author(self,query,api=None,url="https://api.semanticscholar.org/graph/v1/author/search"):
        
        params = {'query':query}
        if api is not None:
            headers = {'X-API-KEY':api}
            req = requests.get(url,params=params,headers=headers)
        else:
            req = requests.get(url,params=params)

        return req.json()
    
    def scholar_search_paper(self,query,api=None,url="https://api.semanticscholar.org/graph/v1/paper/search/match"):
        
        params = {'query':query}
        if api is not None:
            headers = {'X-API-KEY':api}
            req = requests.get(url,params=params,headers=headers)
        else:
            req = requests.get(url,params=params)

        return req.json()
    
    def bulk_papers_retrieval(self,ids,fields,api=None,url='https://api.semanticscholar.org/graph/v1/paper/batch'):

        fields = ','.join(fields)
        params = {'fields':fields}
        all_ids = {'ids':ids}
        
        
        if api is not None:
            
            req = requests.post(url=url,
            params=params,
            headers=headers,
            json=all_ids)
        
        else:
            req = requests.post(url=url,
            params=params,
            json=all_ids)


        return req.json()
    

    def cordis(self,query,url='https://cordis.europa.eu/datalab/sparql-endpoint/en'):
        params = {'query':query,'format':'json'}
        headers = {"Accept": "application/sparql-results+json"}

        req = requests.post(url,params=params,headers=headers)
        return req.text




