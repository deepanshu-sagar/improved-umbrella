def validate_download_all_plat_allow(self, search_url, uri_prefix, token):
    url = 'https://' + uri_prefix + '/heimdall/platformAllowlist/downloadAll'
    headers = {'pubtoken': token}
    response = requests.request('GET', url, headers=headers)
    if response.status_code != 200:
        raise Exception('called downloadAll with token ' + str(token))
    else:
        print('downloadAll completed..!')
    if search_url in response.text:
        print('found')
    else:
        raise Exception('notification is incorrect')