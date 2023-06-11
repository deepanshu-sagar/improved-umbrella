def infra_upload1(self, uri, post_api, file_path):
    url = f'https://{uri}/infrastructure/bulkOperations?{post_api}'
    payload = {}
    headers = {'PubToken': 'token337'}
    files = {'file': open(file_path, 'rb')}
    print(url)
    response = requests.request('POST', url, headers=headers, data=payload, files=files)
    code = response.status_code
    print(code)
    if code == 201:
        import time
        if '/heimdall/publisherWhitelist' in url:
            print('sleeping for 40 sec')
            time.sleep(40)
        elif 'topLevelAdContainer' in url:
            print('sleeping for 40 sec')
            time.sleep(40)
        elif 'publisherAllowlist' in url:
            print('sleeping for 90 sec')
            time.sleep(120)
        else:
            print('sleeping for 20 sec')
            time.sleep(20)