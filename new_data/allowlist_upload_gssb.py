def upload_gssb(self, test_data, db_server, db_port, db_user, db_password, ui_setup, token, activity_db_host, common_db_user_name, common_db_password, common_db_port, uri_prefix, komli_db_host, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, cache_refresh='True'):
    """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
    print(activity_db_host, common_db_user_name, common_db_password, common_db_port)
    upload_content = test_data['upload_content']
    processed_file_data = test_data['processed_file']
    failed_file_data = test_data['failed_file']
    populate_publisher_site_tld_records = test_data['populate_publisher_site_tld_records']
    db_cleanup = str(test_data['db_cleanup']).lower().strip()
    print('db_cleanup flag=' + str(db_cleanup))
    if db_cleanup == 'true':
        start = time.time()
        self.clean_up_gssb(test_data, komli_db_host, db_port, db_user, db_password)
        end = time.time()
        print('Runtime of the upload_gssb is ' + str(end - start))
    if cache_refresh == 'False':
        self.heimdall_cache_refresh(ui_setup, token)
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
    time.sleep(5)
    upload_button = "//button[@data-pm-id='showUploadDomainPopupButton']"
    self.s2l.click_element(upload_button)
    self.s2l.wait_until_element_is_visible("//input[@data-pm-id='file-input']", 60)
    self.acc7.pmccFileUpload('upload-control', file_path)
    print('file selected')
    self.acc7.pmccButton('upload-btn')
    self.wait_for_spinner_to_disappear(120)
    upload_status_xpath = "(//table[@class='pmcc-table pmcc-table-sortable']//tbody//td[text()='{}']//ancestor::tr//span)[2]"
    file_name = os.path.basename(file_path)
    upload_status_xpath = upload_status_xpath.format(file_name)
    upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
    self.refresh = "//button/pmcc-icon[@name='refresh']"
    while upload_status == 'Processing':
        print(upload_status)
        self.s2l.click_element(self.refresh)
        time.sleep(2)
        upload_status = self.s2l.get_webelement(upload_status_xpath).text.strip()
    print('Completed')