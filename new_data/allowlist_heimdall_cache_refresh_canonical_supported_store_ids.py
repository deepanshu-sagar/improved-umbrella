def heimdall_cache_refresh_canonical_supported_store_ids(self, uri, token):
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'canonical.support.valid.store.ids': '3#4#5#6#7#8#999999'})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh_canonical_supported_store_ids with token ' + str(token))
    else:
        print('heimdall_cache_refresh_canonical_supported_store_ids completed..!')