def validate_platform_allowlist_download_all(self, search_url, uri_prefix, token, noti):
    if noti == 'Domain / App ID added successfully.':
        url = 'http://' + uri_prefix + '/heimdall/platformAllowlist/downloadAll'
        headers = {'pubtoken': token}
        response = requests.request('GET', url, headers=headers)
        if response.status_code != 200:
            raise Exception('called downloadAll with token ' + str(token))
        else:
            print('downloadAll completed..!')
        print(response.text)
        if search_url in response.text:
            print('found')
        else:
            BuiltIn().fail('notification is incorrect')
    else:
        print('Nothing to validate in download all.')