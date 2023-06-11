def upload_pub_allowlist_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, ui_setup, token, activity_db_host, common_db_user_name, common_db_password, common_db_port, uri_prefix, user, komli_db_host, spoofer_server_url, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password):
    """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
    print(activity_db_host, common_db_user_name, common_db_password, common_db_port)
    upload_content = test_data['upload_content']
    processed_file_data = test_data['processed_file']
    failed_file_data = test_data['failed_file']
    pixalate_spoofer_data = test_data['pixalate_data']
    populate_publisher_site_tld_records = test_data['populate_publisher_site_tld_records']
    db_cleanup = str(test_data['db_cleanup']).lower().strip()
    print('db_cleanup flag=' + str(db_cleanup))
    if db_cleanup == 'true':
        start = time.time()
        self.clean_up_pub_allowlist_upload_new(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, user)
        end = time.time()
        print('Runtime of the clean_up_allowlist_upload is ' + str(end - start))
    if str(pixalate_spoofer_data) != 'none':
        print('data to add for p&m')
        print(pixalate_spoofer_data)
        m_p_data = pixalate_spoofer_data.split('\n')
        for data in m_p_data:
            file_name = data.split('###')[0]
            pixalate_data = data.split('###')[1]
            self.update_spoofer_response_file(spoofer_server_url, file_name + '_pixelate_spoofer.csv', pixalate_data)
        print('returning from spoofer population')
    else:
        print('nothing to add to p&m')
    self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    self.global_publisher_blocklist_filter_new(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    self.publisher_blocklist_filter(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password)
    self.heimdall_cache_refresh(ui_setup, token)
    self.current_path = os.path.dirname(__file__)
    print('current_path= ' + str(self.current_path))
    letters = string.ascii_lowercase
    file_name = ''.join((random.choice(letters) for i in range(10)))
    file_name = file_name + '.csv'
    file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
    print(file_path)
    with open(file_path, 'w+') as f:
        f.write(str(upload_content))
    self.infra_upload1(ui_setup.split('//')[1], f'resourceUrl=/heimdall/publisherAllowlist?entityId={user}&mode=upload&doIQScan=true', file_path)