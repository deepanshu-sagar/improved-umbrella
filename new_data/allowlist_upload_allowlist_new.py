def upload_allowlist_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, ui_setup, token, komli_db_host, activity_db_host, common_db_user_name, common_db_password, common_db_port, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password, cleanup='True', deleted_data='False', uri_prefix=''):
    """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
    if deleted_data == 'False':
        upload_content = test_data['upload_content']
        processed_file_data = test_data['processed_file']
        failed_file_data = test_data['failed_file']
        populate_publisher_site_tld_records = test_data['populate_publisher_site_tld_records']
        db_cleanup = str(test_data['db_cleanup']).lower().strip()
        if cleanup == 'True':
            print('INSIDE CLEANUP')
            print('DB_CLEANUP:', db_cleanup, ' FIN')
            if db_cleanup == 'true':
                print('INSIDE DB_CLEANUP')
                start = time.time()
                self.clean_up_allowlist_upload_new(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password, komli_db_host, common_db_user_name, common_db_password, common_db_port)
                end = time.time()
            self.hawkeye_app_details_add_del(test_data, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password)
            self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
            self.global_publisher_blocklist_filter_new(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
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
        self.infra_upload(uri_prefix, '/heimdall/adminLevelPublisherAllowlist/', file_path)
    elif deleted_data == 'True':
        upload_content_del = test_data['upload_content_del']
        processed_file_data = test_data['processed_file_del']
        failed_file_data = test_data['failed_file_del']
        if cleanup == 'True':
            if db_cleanup == 'true':
                start = time.time()
                self.clean_up_allowlist_upload_new(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password, komli_db_host, common_db_user_name, common_db_password, common_db_port)
                end = time.time()
            self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
            self.global_publisher_blocklist_filter_new(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
        self.heimdall_cache_refresh(ui_setup, token)
        self.current_path = os.path.dirname(__file__)
        print('current_path= ' + str(self.current_path))
        letters = string.ascii_lowercase
        file_name = ''.join((random.choice(letters) for i in range(10)))
        file_name = file_name + '.csv'
        file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
        print(file_path)
        with open(file_path, 'w+') as f:
            f.write(str(upload_content_del))
        self.infra_upload(uri_prefix, '/heimdall/adminLevelPublisherAllowlist/', file_path)