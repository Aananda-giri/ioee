from django.shortcuts import render
import json
import requests

# Create your views here.
def search(request):
    # get the search query from get request
    query = request.GET.get('search', '')
    
    print(f'\n\n query: {query} \n\n {request}')
    
    if query == '':
        # get the search results from the api
        with open('sample_search_result.json','r') as f:
            search_result = json.load(f)
        query = 'physics'
    else:
        # get results from second api if first api fails
        try:
            search_result = requests.get('http://ec2-18-206-249-251.compute-1.amazonaws.com:5000/search', params={'query': query})
            search_result.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
            search_result = search_result.json()
        except requests.exceptions.HTTPError as err:
            print(f'error: {err}')
            search_result = requests.get('https://strangehacksoldquestionsolution.aanandagiri.repl.co/search', params={'query': query}).json()
        
    return render(request, 'pdf_engine/search.html', {'search_result': search_result})

# requests.get(http://ec2-18-206-249-251.compute-1.amazonaws.com:5000/search', params={'query': 'physics'}).json()['result'][0]
# requests.get('https://strangehacksoldquestionsolution.aanandagiri.repl.co/search', params={'query': 'physics'}).json()['result'][0]