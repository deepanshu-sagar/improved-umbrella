def update_spoofer_response_file(self, spoofer_server_url, file_name, response_txt):
    print('spoof started')
    url = 'http://' + spoofer_server_url + '/updatespoofdata'
    payload = response_txt
    headers = {'file_name': file_name}
    response = requests.request('POST', url, data=payload, headers=headers)
    print('completed')