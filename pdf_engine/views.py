from django.shortcuts import render
import json
import requests

# Create your views here.
def search(request):
    # get the search query from get request
    query = request.GET.get('search', 'physics')
    
    print(f'\n\n query: {query} \n\n {request}')
    
    # get the search results from the api
    # with open('test_search.json','r') as f:
    #     search_result = json.load(f)
    search_result = requests.get('http://ec2-3-88-84-244.compute-1.amazonaws.com:5000/search', params={'query': query}).json()
    # search_result = requests.get('https://strangehacksoldquestionsolution.aanandagiri.repl.co/search', params={'query': query}).json()
    return render(request, 'pdf_engine/search.html', {'search_result': search_result})

# requests.get('http://ec2-3-88-84-244.compute-1.amazonaws.com:5000/search', params={'query': 'physics'}).json()['result'][0]
# requests.get('https://strangehacksoldquestionsolution.aanandagiri.repl.co/search', params={'query': 'physics'}).json()['result'][0]