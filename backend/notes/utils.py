from django.urls import reverse
import random
import string
import json
import base64

def generate_slug(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_url(request, filter_obj, query_param, url):
    stringified = json.dumps(filter_obj)
    encoded = base64.b64encode(bytes(stringified, 'utf-8')).decode('utf-8')

    url_pattern = reverse(url)
    host = request.get_host()
    
    url = 'http://'
    if request.is_secure():
        url = 'https://'
    
    return url+f'{host}{url_pattern}?{query_param}={encoded}'
    
    
        