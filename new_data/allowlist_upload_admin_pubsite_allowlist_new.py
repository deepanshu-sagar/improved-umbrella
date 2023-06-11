def upload_admin_pubsite_allowlist_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, ui_setup, token, Komli_db_server, BulkOps_db_server, activity_db_host, common_db_user_name, common_db_password, common_db_port, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, cleanup='True', deleted_data='False'):
    """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
    import time
    print(activity_db_host, common_db_user_name, common_db_password, common_db_port)
    if deleted_data == 'False':
        upload_content = test_data['upload_content']
        processed_file_data = test_data['processed_file']
        failed_file_data = test_data['failed_file']
        populate_publisher_site_tld_records = test_data['populate_publisher_site_tld_records']
        db_cleanup = str(test_data['db_cleanup']).lower().strip()
        print('db_cleanup flag=' + str(db_cleanup))
        if cleanup == 'True':
            if db_cleanup == 'true':
                start = time.time()
                self.clean_up_pub_site_allowlist_upload_new(test_data, Komli_db_server, BulkOps_db_server, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, common_db_port, common_db_user_name, common_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password)
                end = time.time()
                print('Runtime of the clean_up_allowlist_upload is ' + str(end - start))
            self.hawkeye_app_details_add_del(test_data, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password)
            self.global_channel_partner_blocklist_filter(test_data, Komli_db_server, common_db_port, common_db_user_name, common_db_password)
            self.global_publisher_blocklist_filter_new(test_data, Komli_db_server, common_db_port, common_db_user_name, common_db_password)
            self.platform_allowlist_filter_new(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password)
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
        self.infra_upload(ui_setup.split('//')[1], '/heimdall/publisherWhitelist', file_path)
    elif deleted_data == 'True':
        upload_content_del = test_data['upload_content_del']
        processed_file_data = test_data['processed_file_del']
        failed_file_data = test_data['failed_file_del']
        self.current_path = os.path.dirname(__file__)
        print('current_path= ' + str(self.current_path))
        letters = string.ascii_lowercase
        file_name = ''.join((random.choice(letters) for i in range(10)))
        file_name = file_name + '.csv'
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        print(file_path)
        with open(file_path, 'w+') as f:
            f.write(str(upload_content_del))
        self.infra_upload(ui_setup.split('//')[1], '/heimdall/publisherWhitelist', file_path)