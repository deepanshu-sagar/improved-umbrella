def reProcess_pub_site(self, uri, token):
    import requests
    import json
    url = 'https://ci-va2qa-mgmt.pubmatic.com/heimdall/topLevelAdContainer/reProcess?noOfDays=1'
    payload = {}
    headers = {'pubtoken': '{}'.format(token)}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 202:
        print(response.status_code)
        raise Exception('failed reProcess_pub_site with token ' + str(token))
    else:
        print('reProcess_pub_site completed..!')
    import time
    time.sleep(60)