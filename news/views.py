import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
@api_view(['GET'])
def home(request,usr):
    query = request.data

    url = "https://api.newscatcherapi.com/v2/search"

    querystring = {"q":query,"lang":"en","sort_by":"relevancy","page":"1",}

    headers = {
        "x-api-key": "xQ78CLO795TGElQFTu-nt-_1-uDqmZjenAZxSF2D8E8"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        response_data = response.json()  # Parse the JSON response
        articles = response_data.get('articles')
    
    paginator = Paginator(articles,10)
    content = list(paginator.get_page(1))
    return Response(content)