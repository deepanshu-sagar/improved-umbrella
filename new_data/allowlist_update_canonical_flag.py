def update_canonical_flag(self, test_data, uri, pub_id, fraud_db_host, user_name, password, port):
    if test_data['onboard_canonical_for_ctv'] == 'ON':
        flag = 1
    else:
        flag = 0
    url = f'{uri}/heimdall/canonical/onboarding?pub_id={pub_id}&onboarding_canonical={flag}'
    payload = {}
    headers = {'PubToken': 'token337', 'Content-Type': 'application/json'}
    print(url)
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    assert response.status_code == 200
    self.validate_onboard_canonical_flag_in_db(pub_id, flag, fraud_db_host, user_name, password, port)