def upload_allowlist(self, test_data, db_server, db_port, db_user, db_password, ui_setup, token, komli_db_host, activity_db_host, common_db_user_name, common_db_password, common_db_port):
    """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
    print('test_data=' + str(test_data))
    upload_content = test_data['upload_content']
    populate_publisher_site_tld_records = test_data['populate_publisher_site_tld_records']
    db_cleanup = str(test_data['db_cleanup']).lower().strip()
    print('db_cleanup flag=' + str(db_cleanup))
    if db_cleanup == 'true':
        start = time.time()
        self.clean_up_allowlist_upload(test_data, db_server, db_port, db_user, db_password)
        end = time.time()
        print('Runtime of the clean_up_allowlist_upload is ' + str(end - start))
    start = time.time()
    self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    end = time.time()
    print('Runtime of the global_channel_partner_blocklist_filter is {end - start}')
    start = time.time()
    self.global_publisher_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    end = time.time()
    print('Runtime of the global_publisher_blocklist_filter is ' + str(end - start))
    start = time.time()
    self.heimdall_cache_refresh(ui_setup, token)
    end = time.time()
    print('Runtime of the heimdall_cache_refresh is ' + str(end - start))
    start = time.time()
    self.populate_data(test_data, db_server, db_port, db_user, db_password, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    end = time.time()
    print('Runtime of the populate_data is ' + str(end - start))
    self.current_path = os.path.dirname(__file__)
    print('current_path= ' + str(current_path))
    letters = string.ascii_lowercase
    file_name = ''.join((random.choice(letters) for i in range(10)))
    file_name = file_name + '.csv'
    file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
    f = open(file_path, 'w')
    f.write(str(upload_content))
    f.close()
    print('file_path= ' + str(file_path))
    BuiltIn().log(file_path, level='INFO')
    self.acc7.pmccFileUpload('upload-control', file_path)
    self.acc7.validatePmccFileUpload('upload-control', file_path)
    self.acc7.pmccButton('upload-btn')
    time.sleep(2)
    self.activity_operations_validator(activity_db_host, common_db_port, common_db_user_name, common_db_password, file_name)
    self.activity_file_name = file_name
    start = time.time()
    self.validate_failed_files(ui_setup, token, test_data, db_server, db_port, db_user, db_password)
    end = time.time()
    print('Runtime of the populate_data is ' + str(end - start))
    start = time.time()
    self.validate_allowlist_stats(test_data, db_server, db_port, db_user, db_password)
    end = time.time()
    print('Runtime of the populate_data is ' + str(end - start))