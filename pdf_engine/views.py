from django.shortcuts import render
import json
import requests

# Create your views here.
def search(request):
    # get the search query from get request
    query = request.GET.get('search', '')
    
    print(f'\n\n query: {query} \n\n {request}')
    
    documents_count = 51471   # Todo: display live count like pdfdrive; after implementing live_crawling
    # documents_count = mongo_handler.count_entries()   # Todo: display like pdfdrive

    if query == '':
        # get the search results from the api
        with open('pdf_engine_search_result_physics.json','r') as f:
            search_result = json.load(f)
        query = 'physics'
    else:
        # get results from mongo db
        from pdf_engine.mongo_db_handler import MongoDBHandler
        mongo_handler = MongoDBHandler(collection_name = "pdf_collection", db_name="pdf_engine")
        search_result = mongo_handler.search(query)
        
        # save results fro default query: physics
        # with open("pdf_engine_search_result_physics.json", 'w') as file:
        #     json.dump(list(search_result), file)
        
        
        # get results from second api if first api fails
        # try:
        #     print('try')
        #     search_result = requests.get('https://strangehacksoldquestionsolution.aanandagiri.repl.co/search', params={'query': query})
        #     search_result.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        #     search_result = search_result.json()
            
        #     print(search_result)
        # except Exception as err:
        #     print('except')
        #     print(f'error: {err}')
        #     search_result = requests.get('http://ec2-18-206-249-251.compute-1.amazonaws.com:5000/search', params={'query': query})
        #     search_result.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        #     search_result = search_result.json()
            
        
    return render(request, 'pdf_engine/search.html', {'search_result': search_result, 'query': query, 'documents_count': documents_count})

# requests.get(http://ec2-18-206-249-251.compute-1.amazonaws.com:5000/search', params={'query': 'physics'}).json()['result'][0]
# requests.get('https://strangehacksoldquestionsolution.aanandagiri.repl.co/search', params={'query': 'physics'}).json()['result'][0]