def validate_failed_files(self, api_endpoint, token, test_data, db_server, db_port, db_user, db_password):
    failed_records = test_data['failed_records']
    if str(failed_records).lower().strip() == 'none':
        return
    file_id = self.get_fileid_from_name(db_server, db_port, db_user, db_password)
    print('validating data for file')
    url = str(api_endpoint) + '/infrastructure/bulkOperations/' + str(file_id) + '/failedRecords'
    querystring = {'PubToken': str(token)}
    headers = {'PubToken': str(token), 'cache-control': 'no-cache', 'Postman-Token': '7946c2a1-f182-4913-9f66-ff415d03b5c8'}
    response = requests.request('GET', url, headers=headers, params=querystring)
    api_response = response.text
    print(api_response)
    api_response = str(api_response).split('\n')
    failed_records = failed_records.split('\n')
    print('failed_records= ' + str(failed_records))
    for record in failed_records:
        data = record.split(',')
        domain = data[0]
        failed_description = data[1]
        for domain_item in api_response:
            if str(len(str(domain_item))) == '0':
                continue
            extracted_domain_app = str(domain_item).split(',')[1]
            print(extracted_domain_app)
            if str(extracted_domain_app) == str('"' + domain + '"'):
                print('comparing record')
                print(domain_item)
                print(domain)
                if str(failed_description) in domain_item:
                    print('failure file record is validated ')
                else:
                    print(record)
                    raise Exception('Failed file validation is failed for record ' + str(record))