from django.shortcuts import render
import json
import requests
from pdf_engine.redis_cache import RedisCache

# Create your views here.
def search(request):
    # get the search query from get request
    query = request.GET.get('search', '')
    query = query.strip()
    
    print(f'\n\n query: {query} \n\n {request}')
    
    documents_count = 51471   # Todo: display live count like pdfdrive; after implementing live_crawling
    # documents_count = mongo_handler.count_entries()   # Todo: display like pdfdrive
    if query == '' or query == 'physics':
        # get the search results from the api
        with open('/home/anon/ioee/pdf_engine_search_result_physics.json','r') as f:
            search_results = json.load(f)
        query = 'physics'
    else:
        search_results = RedisCache().get(query)
    # print(f'\n\n search_result: {search_result}')
    return render(request, 'pdf_engine/search.html', {'search_result': search_results, 'query': query, 'documents_count': documents_count})