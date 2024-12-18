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
    
    def scholar_search_paper(self,query,api,url="https://api.semanticscholar.org/graph/v1/paper/search/match"):
        
        params = {'query':query}
        headers = {'X-API-KEY':api}
        req = requests.get(url,params=params,headers=headers)

        return req.json()
    
    def bulk_papers_retrieval(self,ids,api,fields,url='https://api.semanticscholar.org/graph/v1/paper/batch'):

        fields = ','.join(fields)
        params = {'fields':fields}
        all_ids = {'ids':ids}
        headers = {'X-API-KEY':api}
        

        #req = requests.post(url,params,json=all_ids)
        req = requests.post(url=url,
        params=params,
        headers=headers,
        json=all_ids)

        return req.json()
    

    def cordis_extraction(self,params={'query':"contenttype='project' AND (programme/code='H2020') AND 'rocket'",'outputFormat':'json','key':''},url='https://cordis.europa.eu/api/dataextractions/getExtraction'):
        params = params

        req = requests.get(url,params=params)

        return req.json()
    
    def cordis_extraction_list(self,params={'key':''},url='https://cordis.europa.eu/api/dataextractions/listExtractions'):
        params = params

        req = requests.get(url,params=params)
        tasksUrls = [x['destinationFileUri'] for x in req.json()['payload']['result']]
        
        return tasksUrls

    




