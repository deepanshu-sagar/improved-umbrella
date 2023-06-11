def validate_download_all_pub_allow(self, search_url, uri_prefix, token, user):
    url = 'https://' + uri_prefix + '/heimdall/publisherAllowlist/download?pageNumber=1&pageSize=10&pubId={1}&query=adservingEntity:{0},pubId:{1},'.format(search_url, user)
    headers = {'pubtoken': token}
    response = requests.request('GET', url, headers=headers)
    if response.status_code != 200:
        raise Exception('called downloadAll with token ' + str(token))
    else:
        print('downloadAll completed..!')
    if search_url in response.text:
        print('validate_download_all_pub_allow completed : found')
    else:
        raise Exception('notification is incorrect')