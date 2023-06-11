def topLevelAdContainer_updateCTVApps(self, uri, token):
    import requests
    import json
    url = 'https://{}/heimdall/topLevelAdContainer/updateCTVApps?pubIdsLimit=100&recordLimit=5000'.format(uri)
    payload = {}
    headers = {'pubtoken': '{}'.format(token)}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 202:
        print(response.status_code)
        raise Exception('failed topLevelAdContainer_updateCTVApps with token ' + str(token))
    else:
        print('topLevelAdContainer_updateCTVApps completed..!')