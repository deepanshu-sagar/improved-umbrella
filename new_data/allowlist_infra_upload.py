def infra_upload(self, uri, post_api, file_path):
    url = f'https://{uri}/infrastructure/bulkOperations?mode=upload&resourceUrl={post_api}?entityId=0'
    payload = {}
    headers = {'PubToken': 'token337'}
    with open(file_path, 'rb') as f:
        data = f.read()
    print(data)
    files = {'file': open(file_path, 'rb')}
    print(url)
    print(headers)
    print(payload)
    print(files)
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
        else:
            print('sleeping for 20 sec')
            time.sleep(20)
    else:
        assert response.status_code == 201