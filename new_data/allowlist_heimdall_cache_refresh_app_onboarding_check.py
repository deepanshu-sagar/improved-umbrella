def heimdall_cache_refresh_app_onboarding_check(self, uri, token, value):
    import requests
    import json
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'allowlisting.ctv.app.onboarding.check': '{}'.format(value)})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh with token ' + str(token))
    else:
        print('heimdall_cache_refresh completed..!')