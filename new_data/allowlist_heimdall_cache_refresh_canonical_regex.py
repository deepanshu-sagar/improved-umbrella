def heimdall_cache_refresh_canonical_regex(self, uri, token):
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    print(url)
    payload = json.dumps({'canonical.regex.validation.3': '^[0-9]+$', 'canonical.regex.validation.4': '^[0-9]+$', 'canonical.regex.validation.5': '^[a-zA-Z0-9]+$', 'canonical.regex.validation.6': '^[0-9]+$', 'canonical.regex.validation.7': '^[a-zA-Z.]+$', 'canonical.regex.validation.8': '^[a-zA-Z0-9]+$', 'canonical.regex.validation.9': '^[a-zA-Z.]+$'})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_app_Config_cache_refresh with token ' + str(token))
    else:
        print('heimdall_app_Config_cache_refresh completed..!')