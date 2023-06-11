def heimdall_cache_refresh(self, api_endpoint, token):
    url = str(api_endpoint) + '/heimdall/cache-refresh'
    payload = ''
    headers = {'Content-Type': 'application/json', 'pubtoken': str(token), 'cache-control': 'no-cache', 'Postman-Token': '604f3d8a-f148-49e1-ba8d-e79416b77e74'}
    response = requests.request('GET', url, data=payload, headers=headers)
    print(response.text)