from django.shortcuts import render
import json
import requests

# Create your views here.
def search(request):
    # get the search query from get request
    query = request.GET.get('search', '')
    query = query.strip()
    
    print(f'\n\n query: {query} \n\n {request}')
    
    documents_count = 51471   # Todo: display live count like pdfdrive; after implementing live_crawling
    # documents_count = mongo_handler.count_entries()   # Todo: display like pdfdrive
    search_result = []
    if query == '' or query == 'physics':
        # get the search results from the api
        with open('pdf_engine_search_result_physics.json','r') as f:
            search_result = json.load(f)
        query = 'physics'
    else:
        # get results from mongo db
        from pdf_engine.mongo_db_handler import MongoDBHandler
        mongo_handler = MongoDBHandler(collection_name = "pdf_collection", db_name="pdf_engine")
        try:
            search_result = list(mongo_handler.search(query))
        except:
            # search_result is empty
            search_result = []
        
        # save results fro default query: physics
        # with open("pdf_engine_search_result_physics.json", 'w') as file:
        #     json.dump(list(search_result), file)
        
        
    # print(f'\n\n search_result: {search_result}')
    return render(request, 'pdf_engine/search.html', {'search_result': search_result, 'query': query, 'documents_count': documents_count})