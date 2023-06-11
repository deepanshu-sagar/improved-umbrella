def __init__(self):
    """
        Constructor
        """
    BasePage.__init__(self)
    self.sw = SeleniumWrapper()
    self.acc7 = AngularCoreComponents7()
    self.activity_file_name = 'mqbecltpsb.csv'
    print('init..')
    self.DB = AllowlistDB()

def logout_from_admin(self):
    """
        Logout on Admin Page
        :return:
        """
    headerXpath = '//pmac-header'
    userInfoXpath = headerXpath + "//*[@data-pm-id='gh-user-info']"
    logOutXpath = headerXpath + "//*[@data-pm-id='gh-log-out']"
    default_timeout = self.s2l.set_selenium_implicit_wait(2)
    self.s2l.element_should_be_visible(headerXpath)
    self.s2l.element_should_be_visible(userInfoXpath)
    self.s2l.click_element(userInfoXpath)
    self.s2l.element_should_be_visible(logOutXpath)
    self.s2l.click_element(logOutXpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)

def logout_publisher_via_admin(self):
    """
        Logout from Publisher
        :return:
        """
    headerXpath = '//pmac-header'
    userInfoXpath = headerXpath + "//*[@data-pm-id='gh-user-info']"
    logOutXpath = headerXpath + "//*[@data-pm-id='gh-log-out']"
    default_timeout = self.s2l.set_selenium_implicit_wait(2)
    self.s2l.select_window('MAIN')
    self.s2l.element_should_be_visible(headerXpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)
    self.s2l.element_should_be_visible(userInfoXpath)
    self.s2l.click_element(userInfoXpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)
    self.s2l.element_should_be_visible(logOutXpath)
    self.s2l.click_element(logOutXpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)

def search_and_login_as_publisher(self, pub_id):
    """
        search publisher and login
        :param pub_id: publisher id to login with
        :return: None
        """
    pub_id = unicode(pub_id)
    default_timeout = self.s2l.set_selenium_implicit_wait(2)
    search_pub_xpath = "//pmcc-input/input[@data-pm-id='search-pub']"
    search_btn_xpath = "//button[@data-pm-id='search-btn']"
    radio_btn_xpath = "//*[@data-pm-id='radio-" + pub_id + "']"
    login_pub_btn_xpath = "//*[@data-pm-id='login']"
    dashboard_title_xpath = "(//h1[contains(text(), 'Dashboard')])[1] | //h1//*[contains(text(), 'Dashboard')]"
    BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'click_element', search_pub_xpath)
    self.s2l.input_text(search_pub_xpath, pub_id)
    self.s2l.click_element(search_btn_xpath)
    BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'element_should_be_visible', radio_btn_xpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)
    self.s2l.click_element(radio_btn_xpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)
    self.s2l.click_element(login_pub_btn_xpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)
    self.s2l.select_window('NEW')
    BuiltIn().wait_until_keyword_succeeds('150 sec', '2 sec', 'element_should_be_visible', dashboard_title_xpath)

def login_as_publisher_via_admin(self, admin_login_id, admin_password, pub_id, okta_username=None, okta_password=None, timeout=60):
    """
        Method to login to publisher via admin
        :param admin_login_id: admin username
        :param admin_password: admin password
        :param pub_id:
        :param okta_username:
        :param okta_password:
        :param timeout:
        :return:
        """
    self.login_as_admin(admin_login_id, admin_password, okta_username, okta_password, timeout=timeout)
    self.search_and_login_as_publisher(pub_id)

def login_as_admin(self, admin_login_id, admin_password, okta_username='None', okta_password=None, login_type='Publisher', timeout=60):
    """
        Method to login with admin
        :param admin_login_id: username
        :param admin_password: password
        :return:
        """
    default_timeout = self.s2l.set_selenium_implicit_wait(1)
    username_xpath = '//*[@id="okta-signin-username"]'
    password_xpath = '//*[@id="okta-signin-password"]'
    login_btn_xpath = '//*[@id="okta-signin-submit"]'
    okta_username_xpath = '//*[@id="okta-signin-username"]'
    okta_password_xpath = '//*[@id="okta-signin-password"]'
    okta_submit_xpath = '//*[@id="okta-signin-submit"]'
    search_pub_title_xpath = "//*[@class='pmcc-page-content']//h1"
    campaign_manager_xpath = '//div/h1'
    self.s2l.maximize_browser_window()
    start_time = time.time()
    okta_connecting = '(//h1)[1]'
    BuiltIn().wait_until_keyword_succeeds('240 sec', '5 sec', 'element_should_contain', okta_connecting, 'Connecting to')
    is_okta_login_page = BuiltIn().run_keyword_and_return_status('Click Element', okta_username_xpath)
    print('okta')
    print(is_okta_login_page)
    if is_okta_login_page:
        print('okta page')
        self.s2l.input_text(okta_username_xpath, 'user_302@pubmatic.com')
        self.s2l.input_text(okta_password_xpath, 'Asdf@123')
        self.s2l.click_element(okta_submit_xpath)
        print('okta login clicked')
        print('checking status')
        BuiltIn().wait_until_keyword_succeeds('120 sec', '1 sec', 'Click Element', username_xpath)
        print('checking status done')
    admin_page = '(//h2)[1]'
    BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain', admin_page, 'Log In to Your Account')
    is_admin_page = BuiltIn().run_keyword_and_return_status('Click Element', username_xpath)
    is_admin_page = True
    print('is_admin_page=' + str(is_admin_page))
    if is_admin_page:
        print('in admin login flow')
        print(admin_login_id)
        self.s2l.input_text(username_xpath, admin_login_id)
        self.s2l.input_text(password_xpath, admin_password)
        self.s2l.click_element(login_btn_xpath)
        if login_type == 'Publisher':
            BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain', search_pub_title_xpath, 'Search Publisher')
        elif login_type == 'Admin':
            BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain', search_pub_title_xpath, 'Search Publisher')
        elif login_type == 'Demand':
            BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_contain', campaign_manager_xpath, 'Campaign Manager')
    print('exiting login method')
    self.s2l.set_selenium_implicit_wait(default_timeout)

def navigate_to(self, menu_identifier, sub_menu_identifier):
    """
        Method to navigate to page
        :param menu_identifier:
        :param sub_menu_identifier:
        :return:
        """
    default_timeout = self.s2l.set_selenium_implicit_wait(2)
    menuXpath = "//*[@data-pm-id='{}']".format(menu_identifier)
    subMenuXpath = "//*[@data-pm-id='{}']".format(sub_menu_identifier)
    BuiltIn().wait_until_keyword_succeeds('120 sec', '2 sec', 'element_should_be_visible', menuXpath)
    self.s2l.element_should_be_visible(menuXpath)
    self.s2l.click_element(menuXpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)
    self.s2l.element_should_be_visible(subMenuXpath)
    self.s2l.click_element(subMenuXpath)
    self.s2l.set_selenium_implicit_wait(default_timeout)

def open_browser_with_download_capabilities(self, url, browser='gc', remote_url=None):
    """

        :param url:
        :param browser:
        :param remote_url:
        :return:
        """
    driver = None
    if remote_url is not None:
        if browser.lower() == 'gc' or browser.lower() == 'chrome':
            driver = Remote(remote_url, self.CHROME_CAPABILITIES)
        else:
            pass
    elif browser.lower() == 'gc' or browser.lower() == 'chrome':
        driver = Chrome(desired_capabilities=self.CHROME_CAPABILITIES)
    else:
        pass
    driver.get(url)
    driver.set_script_timeout(30)
    self.s2l.register_driver(driver, alias='wd')

def verify_page_title(self):
    print('cheking page title and components')

def execute_sql_db_multi(self, sql, db_server, db_user, db_password, db_port, db):
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), port=str(db_port), passwd=str(db_password), database=str(db))
    mycursor = mydb.cursor()
    select_out = []
    for result in mycursor.execute(sql, multi=True):
        if result.with_rows:
            out = result.fetchall()
            select_out.append(out)
        else:
            pass
    mydb.commit()
    return select_out

def activity_operations_validator(self, db_server, db_port, db_user, db_password, file_name):
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), port=str(db_port), passwd=str(db_password), database='ActivityLog')
    flag = False
    for i in range(1, 200):
        mycursor = mydb.cursor()
        sql = "select status  from bulk_operations where  file_name ='" + str(file_name) + "'; "
        print(sql)
        mycursor.execute(sql)
        data = mycursor.fetchone()
        if isinstance(data, tuple):
            for x in data:
                print(x)
                if x == '1':
                    flag = True
        if flag == True:
            print('bulk operation validated!')
            return
        time.sleep(1)
        print('sleeping')
        mydb.commit()
    raise Exception('bulk operation failed!')

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

def upload_plat_allowlist_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, ui_setup, token, activity_db_host, common_db_user_name, common_db_password, common_db_port, uri_prefix, komli_db_host, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, cache_refresh='True'):
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
        self.clean_up_plat_allowlist_upload_new(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password)
        end = time.time()
        print('Runtime of the clean_up_allowlist_upload is ' + str(end - start))
    if cache_refresh == 'False':
        self.heimdall_cache_refresh(ui_setup, token)
    self.hawkeye_app_details_add_del(test_data, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password)
    self.global_channel_partner_blocklist_filter(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    self.global_publisher_blocklist_filter_new(test_data, komli_db_host, common_db_port, common_db_user_name, common_db_password)
    self.insert_app_details(test_data, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password)
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
    self.infra_upload(uri_prefix, '/heimdall/bulkPlatformAllowlist', file_path)

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

def upload_pub_site_allowlist_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, ui_setup, Komli_db_server, BulkOps_db_server, activity_db_host, common_db_user_name, common_db_password, common_db_port, uri_prefix, token, user, spoofer_server_url, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password):
    """
        Method to upload file for margin settings
        :param upload_file_name: file name for uploading
        :return:
        """
    upload_content = test_data['upload_content']
    processed_file_data = test_data['processed_file']
    failed_file_data = test_data['failed_file']
    pixalate_spoofer_data = test_data['pixalate_data']
    self.global_channel_partner_blocklist_filter(test_data, Komli_db_server, common_db_port, common_db_user_name, common_db_password)
    self.global_publisher_blocklist_filter_new(test_data, Komli_db_server, common_db_port, common_db_user_name, common_db_password)
    self.platform_allowlist_filter_new(test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password)
    self.heimdall_cache_refresh(ui_setup, token)
    populate_publisher_site_tld_records = test_data['populate_publisher_site_tld_records']
    db_cleanup = str(test_data['db_cleanup']).lower().strip()
    print('db_cleanup flag=' + str(db_cleanup))
    if db_cleanup == 'true':
        start = time.time()
        self.clean_up_pub_pub_site_allowlist_upload_new(test_data, Komli_db_server, BulkOps_db_server, common_db_port, common_db_user_name, common_db_password, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, user)
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
    self.current_path = os.path.dirname(__file__)
    print('current_path= ' + str(current_path))
    letters = string.ascii_lowercase
    file_name = ''.join((random.choice(letters) for i in range(10)))
    file_name = file_name + '.csv'
    file_path = OperatingSystem().normalize_path(os.path.join(self.current_path, file_name))
    print('file_path= ' + str(file_path))
    with open(file_path, 'w+') as f:
        f.write(str(upload_content))
    self.infra_upload1(ui_setup.split('//')[1], f'resourceUrl=/heimdall/topLevelAdContainer/?entityId={user}&mode=upload&doIQScan=true', file_path)

def validate_plat_ui_table(self, test_data, db_user_name, db_password, db_host, db_port, activity_logs_db_user_name, activity_logs_db_password, activity_logs_db_host, activity_logs_db_port, uri_prefix, token):
    self.find_domain_platform_allowlist(test_data.split(',')[0])
    df_db = self.get_platform_allowlist_db_data(test_data.split(',')[0], db_user_name, db_password, db_host, int(db_port))
    print('dataframe database')
    print(df_db)
    print(test_data.split(',')[1])
    if test_data.split(',')[1] != 'CTV':
        print(test_data.split(',')[1])
        crc_64 = self.calculate_crc64(test_data.split(',')[0])
        print(str(crc_64))
    else:
        if test_data.split(',')[2] == 'Roku':
            store = '3'
        else:
            store = '999999'
        crc = '{0}_{1}'.format(store, test_data.split(',')[0])
        crc_64 = self.calculate_crc64(crc)
        print(crc_64)
    df_db.rename(columns={'domain': 'Domain / App ID', 'platform_id': 'Platform', 'store_id': 'Store'}, inplace=True)
    df_ui = self.acc7.pmccTable('dt-table')
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop('Last Modified', axis=1)
    print('DB DATAFRAME')
    BuiltIn().log(df_db)
    print('UI DATAFRAME')
    BuiltIn().log(df_ui)
    self.search_in_df(df_ui, df_db)
    self.validate_download_all_plat_allow(test_data.split(',')[0], uri_prefix, token)

def validate_publisher_ui_table(self, test_data, db_user_name, db_password, db_host, db_port, activity_logs_db_user_name, activity_logs_db_password, activity_logs_db_host, activity_logs_db_port, uri_prefix, token, user):
    self.find_domain_publisher_allowlist(test_data.split(',')[0])
    print('find completed')
    df_db = self.get_publisher_allowlist_db_data(test_data.split(',')[0], db_user_name, db_password, db_host, int(db_port))
    print('dataframe database')
    print(df_db)
    print(test_data.split(',')[1])
    if test_data.split(',')[1] != 'CTV':
        print(test_data.split(',')[1])
        crc_64 = self.calculate_crc64(test_data.split(',')[0])
        print(str(crc_64))
    else:
        if test_data.split(',')[2] == 'Roku':
            store = '3'
        else:
            store = '999999'
        crc = '{0}_{1}'.format(store, test_data.split(',')[0])
        crc_64 = self.calculate_crc64(crc)
        print(crc_64)
    df_db.rename(columns={'domain': 'Domain / App ID', 'platform_id': 'Platform', 'store_id': 'Store'}, inplace=True)
    df_ui = self.acc7.pmccTable('dt-table')
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop('Status', axis=1)
    df_ui = df_ui.drop('Error Description', axis=1)
    print('DB DATAFRAME')
    print(df_db)
    print('UI DATAFRAME')
    print(df_ui)
    self.search_in_df(df_ui, df_db)
    self.validate_download_all_pub_allow(test_data.split(',')[0], uri_prefix, token, user)

def validate_view_domain_ui_table(self, test_data, db_user_name, db_password, db_host, db_port, uri_prefix, token, user):
    print('validate_view_domain_ui_table')
    self.wait_for_spinner_to_disappear(100)
    site_search = "//input[@id='search']"
    self.s2l.input_text(site_search, test_data.split(',')[0])
    self.s2l.press_key(site_search, u'\\13')
    self.wait_for_spinner_to_disappear(100)
    time.sleep(5)
    view_domain_action = "(//pmcc-icon[@data-pm-id='table-action-btn'])[2]"
    self.s2l.click_element(view_domain_action)
    view_domains = "//li[.='View Domains']"
    self.s2l.click_element(view_domains)
    self.wait_for_spinner_to_disappear(100)
    self.find_domain_publisher_site_allowlist(test_data.split(',')[1])
    print('view domain search completed')
    df_db = self.get_publisher_site_allowlist_db_data(test_data.split(',')[1], user, db_user_name, db_password, db_host, int(db_port))
    print('dataframe database')
    print(df_db)
    print(test_data.split(',')[1])
    if test_data.split(',')[1] != 'CTV':
        print(test_data.split(',')[1])
        crc_64 = self.calculate_crc64(test_data.split(',')[0])
        print(str(crc_64))
    else:
        if test_data.split(',')[2] == 'Roku':
            store = '3'
        else:
            store = '999999'
        crc = '{0}_{1}'.format(store, test_data.split(',')[0])
        crc_64 = self.calculate_crc64(crc)
        print(crc_64)
    df_ui = self.acc7.pmccTable('dt-table')
    df_ui = df_ui.drop([''], axis=1)
    print('DB DATAFRAME')
    print(df_db)
    print('UI DATAFRAME')
    print(df_ui)
    self.search_in_df(df_ui, df_db)
    filtered_allowlist = "//button[text()=' Filtered Allowlist ']"
    filtered_allowlist_df = self.download_file_and_get_DF(filtered_allowlist)
    print('filtered_allowlist df')
    print(filtered_allowlist_df)
    filtered_allowlist_df = filtered_allowlist_df.drop(['Site Identifier'], axis=1)
    filtered_allowlist_df = filtered_allowlist_df.drop(['Platform (Web/Mobile Web/Mobile App iOS/Mobile App Android/CTV)'], axis=1)
    filtered_allowlist_df['Description'] = filtered_allowlist_df['Description'].replace(np.nan, '')
    filtered_allowlist_df['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'] = filtered_allowlist_df['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'].replace(np.nan, 0)
    filtered_allowlist_df = filtered_allowlist_df.rename(columns={'Domain/App Store URL/CTV App ID/App ID/Bundle ID': 'Domain Name'})
    print('modified filtered_allowlist df')
    print(filtered_allowlist_df)
    self.search_in_df(filtered_allowlist_df, df_db)
    self.s2l.reload_page()
    go_back = "//button[text()=' Go Back ']"
    self.s2l.click_element(go_back)
    time.sleep(5)
    self.wait_for_spinner_to_disappear(100)

def validate_download_all_plat_allow(self, search_url, uri_prefix, token):
    url = 'https://' + uri_prefix + '/heimdall/platformAllowlist/downloadAll'
    headers = {'pubtoken': token}
    response = requests.request('GET', url, headers=headers)
    if response.status_code != 200:
        raise Exception('called downloadAll with token ' + str(token))
    else:
        print('downloadAll completed..!')
    if search_url in response.text:
        print('found')
    else:
        raise Exception('notification is incorrect')

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

def find_domain_platform_allowlist(self, domain_name):
    """
        Searches for a domain using Search Box on UI
        :param domain_name: unicode string
        :return: None
        """
    self.search_domain = "//input[@data-pm-id='search-domain-input']"
    if domain_name is not None and domain_name != '':
        domain_name = unicode(domain_name)
        self.s2l.input_text(self.search_domain, domain_name)
        self.s2l.press_key(self.search_domain, u'\\13')
        self.wait_for_spinner_to_disappear(60)
    else:
        BuiltIn().log('Search Domain Function should be called in case of searching with Substring or Exact name', level='WARN')

def find_domain_publisher_allowlist(self, domain_name):
    """
        Searches for a domain using Search Box on UI
        :param domain_name: unicode string
        :return: None
        """
    self.search_domain = "//input[@data-pm-id='search-domain-app-id-input']"
    if domain_name is not None and domain_name != '':
        domain_name = unicode(domain_name)
        self.s2l.input_text(self.search_domain, domain_name)
        self.s2l.press_key(self.search_domain, u'\\13')
        self.wait_for_spinner_to_disappear(60)
    else:
        BuiltIn().log('Search Domain Function should be called in case of searching with Substring or Exact name', level='WARN')

def find_domain_publisher_site_allowlist(self, domain_name):
    """
        Searches for a domain using Search Box on UI
        :param domain_name: unicode string
        :return: None
        """
    print('find_domain_publisher_site_allowlist')
    self.search_domain = "//input[@id='search']"
    if domain_name is not None and domain_name != '':
        domain_name = unicode(domain_name)
        self.s2l.input_text(self.search_domain, domain_name)
        self.s2l.press_key(self.search_domain, u'\\13')
        self.wait_for_spinner_to_disappear(60)
    else:
        BuiltIn().log('Search Domain Function should be called in case of searching with Substring or Exact name', level='WARN')

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

def get_platform_allowlist_db_data(self, tld_names, db_user, db_password, db_host, port):
    """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
    mydb = mysql.connector.connect(host=str(db_host), user=str(db_user), passwd=str(db_password), port=str(port), database='fraud_mgmt')
    rows_query = "SELECT adserving_entity as 'Domain / App ID', platform_id as Platform, store_id as Store FROM fraud_mgmt.platform_allowlist WHERE adserving_entity ='{}';".format(tld_names)
    all_df = pd.read_sql(rows_query, mydb)
    platform_replace_values = {1: 'WEB', 2: 'MOBILE_WEB', 4: 'MOBILE_APP_IOS', 5: 'MOBILE_APP_ANDROID', 7: 'CTV'}
    store_id_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
    all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
    all_df['Store'] = all_df['Store'].map(store_id_replace_values)
    print(all_df)
    return all_df

def get_publisher_allowlist_db_data(self, tld_names, db_user, db_password, db_host, port):
    """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
    print('running get_publisher_allowlist_db_data')
    mydb = mysql.connector.connect(host=str(db_host), user=str(db_user), passwd=str(db_password), port=str(port), database='fraud_mgmt')
    rows_query = "SELECT adserving_entity as 'Domain / App ID', platform_id as Platform, store_id as Store FROM fraud_mgmt.publisher_allowlist WHERE adserving_entity ='{}';".format(tld_names)
    print(rows_query)
    all_df = pd.read_sql(rows_query, mydb)
    platform_replace_values = {1: 'Web', 2: 'Mobile Web', 4: 'Mobile App IOS', 5: 'Mobile App Android', 7: 'CTV'}
    store_id_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
    all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
    all_df['Store'] = all_df['Store'].map(store_id_replace_values)
    print(all_df)
    return all_df

def get_publisher_site_allowlist_db_data(self, tld_names, user, db_user, db_password, db_host, port):
    """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
    mydb = mysql.connector.connect(host=str(db_host), user=str(db_user), passwd=str(db_password), port=str(port), database='BulkOpsMgmt')
    rows_query = "SELECT tld_name as 'Domain Name', status as Status, store_id as 'CTV App Store', description as Description FROM BulkOpsMgmt.staging_publisher_aggregator_site_tld WHERE tld_name ='{0}' and pub_id= {1};".format(tld_names, str(user))
    print(rows_query)
    all_df = pd.read_sql(rows_query, mydb)
    status_replace_values = {0: 'Approved'}
    store_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
    all_df['Status'] = all_df['Status'].map(status_replace_values)
    all_df['CTV App Store'] = all_df['CTV App Store'].map(store_replace_values)
    print(all_df)
    return all_df

def download_file_and_get_DF(self, path):
    self.download_dir = os.path.normpath(os.path.join(current_path, '..', '..', 'Downloads'))
    file_path = self.click_and_wait_for_download_to_complete(download_link_xpath=path, default_download_dir=self.download_dir)
    return pd.read_csv(file_path)

def click_and_wait_for_download_to_complete(self, download_link_xpath=None, default_download_dir=None, start_wait_timeout=30, retry_interval=5, function_to_exec=None, hoverable_xpath=None, **params):
    """

        :param download_link_xpath:
        :param default_download_dir:
        :param start_wait_timeout:
        :param retry_interval:
        :param function_to_exec:
        :param params:
        :param hoverable_xpath:
        :return:
        """
    if download_link_xpath is None and function_to_exec is None:
        BuiltIn().fail('One of the parameter is required (download_link_xpath, default_download_dir)\nNone of the metioned parameters were passed')
    elif download_link_xpath is not None and function_to_exec is not None:
        BuiltIn().fail('Both download_link_xpath and function_to_exec passed.\nPlease pass one of the two options')
    if default_download_dir is None:
        BuiltIn().fail('Default download directory is compulsory field. Pass a valid Directory Path')
    elif not os.path.isdir(default_download_dir):
        BuiltIn().fail('default_download_dir value passed is not a valid directory')
    current_window_handle = self.s2l.driver.current_window_handle
    try:
        browser_version = int(self.s2l.driver.capabilities['version'].split('.')[0])
    except (KeyError, AttributeError, IndexError):
        browser_version = int(self.s2l.driver.capabilities.get('browserVersion').split('.')[0])

    def get_all_file_in_download_manager():
        """
            :return:
            """
        new_tab_query = "window.open('')"
        if not self.s2l.get_location().startswith('chrome://downloads'):
            self.s2l.execute_javascript(new_tab_query)
            time.sleep(2)
            self.s2l.switch_window('NEW')
            self.s2l.go_to('chrome://downloads')
        if browser_version >= 80:
            return self.s2l.execute_javascript("\n                return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList').items;\n                ")
        else:
            return self.s2l.execute_javascript('\n                                return downloads.Manager.get().items_;\n                                ')

    def get_download_state_by_id(id):
        """

            :param id:
            :return:
            """
        if browser_version >= 80:
            script = "return document.querySelector('downloads-manager').shadowRoot\n                .querySelector('#downloadsList').items.filter(e => e.id === '{id}').map(e => e.state);".format(id=id)
        else:
            script = "return downloads.Manager.get().items_.filter(e => e.id === '{id}').map(e => e.state);".format(id=id)
        return self.s2l.execute_javascript(script)[0]

    def get_file_content(path):
        elem = self.s2l.driver.execute_script("var input = window.document.createElement('INPUT'); input.setAttribute('type', 'file'); input.hidden = true; input.onchange = function (e) { e.stopPropagation() }; return window.document.documentElement.appendChild(input); ")
        elem._execute('sendKeysToElement', {'value': [path], 'text': path})
        result = self.s2l.driver.execute_async_script('var input = arguments[0], callback = arguments[1]; var reader = new FileReader(); reader.onload = function (ev) { callback(reader.result) }; reader.onerror = function (ex) { callback(ex.message) }; reader.readAsDataURL(input.files[0]); input.remove(); ', elem)
        if not result.startswith('data:'):
            raise Exception('Failed to get file content: %s' % result)
        return base64.b64decode(result[result.find('base64,') + 7:])
    files_before_download = get_all_file_in_download_manager()
    previous_ids = [e['id'] for e in files_before_download]
    current_time = time.time()
    self.s2l.close_window()
    self.s2l.switch_window(current_window_handle)
    if not hoverable_xpath is None:
        self.s2l.mouse_over(hoverable_xpath)
        self.s2l.wait_until_element_is_visible(download_link_xpath, 60)
    if download_link_xpath is not None:
        self.s2l.click_element(download_link_xpath)
    else:
        function_to_exec(**params)
    new_file_download_id = None
    while new_file_download_id is None and time.time() - current_time < start_wait_timeout:
        files_list_after_click = get_all_file_in_download_manager()
        current_ids = [e['id'] for e in files_list_after_click]
        if len(set(current_ids).difference(previous_ids)) == 1:
            new_file_download_id = list(set(current_ids).difference(previous_ids))[0]
            print(new_file_download_id)
            break
        elif len(set(current_ids).difference(previous_ids)) > 1:
            BuiltIn().fail("Multiple Download started with IDs: '{}'".format(set(current_ids).difference(previous_ids)))
        else:
            time.sleep(retry_interval)
    if new_file_download_id is None:
        BuiltIn().fail('Cannot Start Downloading After waiting for {} seconds'.format(start_wait_timeout))
    else:
        time.sleep(retry_interval)
        download_state = get_download_state_by_id(new_file_download_id)
        while download_state == 'IN_PROGRESS':
            time.sleep(retry_interval)
            download_state = get_download_state_by_id(new_file_download_id)
            print('Download state: {}'.format(download_state))
        if download_state == 'COMPLETE':
            all_files = get_all_file_in_download_manager()
            file_path = [f['file_path'] if 'file_path' in f.keys() else f['filePath'] for f in filter(lambda e: e['id'] == new_file_download_id, all_files)][0]
            file_content = get_file_content(file_path)
            new_file_location = os.path.normpath(os.path.join(default_download_dir, os.path.basename(file_path)))
            print('Copying File to: {}'.format(new_file_location))
            with open(new_file_location, 'wb') as fp:
                fp.write(file_content)
        else:
            BuiltIn().fail('File download is not in progress and neither completed. Current State: {}'.format(download_state))
    self.s2l.close_window()
    self.s2l.switch_window(current_window_handle)
    return new_file_location

def delete_BulkOps(self, fileName, db_host, db_user_name, db_password, db_port):
    self.DB.delete_BulkOps_db_data(fileName, db_host, db_user_name, db_password, int(db_port))

def update_oo(self, db_host, db_user_name, db_password, db_port, user, value):
    self.DB.update_oo(db_host, db_user_name, db_password, int(db_port), user, value)

def update_pub_blocklist(self, db_host, db_user_name, db_password, db_port, user, value):
    self.DB.update_pub_blocklist(db_host, db_user_name, db_password, int(db_port), user, value)

def validate_admin_pub_upload(self, data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, oo=-1):
    self.DB.validate_admin_pub_upload(data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, oo)
    self.DB.validate_storeName_in_store_urls(data, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password)

def validate_admin_pub_upload_deleted(self, data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, oo=-1):
    self.DB.validate_admin_pub_upload_deleted(data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, oo)

def validate_admin_pub_site_upload(self, data, Bulk_db, Komli_db, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, common_db_user_name, common_db_password, common_db_port, user, oo=-1):
    self.DB.validate_admin_pub_site_upload(data, Bulk_db, Komli_db, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, common_db_user_name, common_db_password, common_db_port, user, oo)

def validate_updated_crc_888888(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user):
    self.DB.validate_updated_crc_888888(data, db_host, Bulk_db, Komli_db, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user)

def update_crc_to_0_pub_site(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user):
    self.DB.update_crc_to_0_pub_site(data, db_host, Bulk_db, Komli_db, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user)

def update_store_id_0_pub_site(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user):
    self.DB.update_store_id_0_pub_site(data, db_host, Bulk_db, Komli_db, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user)

def update_status_to_6_pub_site(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user):
    self.DB.update_status_to_6_pub_site(data, db_host, Bulk_db, Komli_db, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user)

def update_updatetime_pub_site(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user, updatetime):
    self.DB.update_updatetime_pub_site(data, db_host, Bulk_db, Komli_db, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user, updatetime)

def update_updatetime_all_pub_site(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user, updatetime):
    self.DB.update_updatetime_all_pub_site(data, db_host, Bulk_db, Komli_db, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user, updatetime)

def update_status_to_6_pub(self, data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port):
    self.DB.update_status_to_6_pub(data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port)

def update_updatetime_pub(self, data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, updatetime):
    self.DB.update_updatetime_pub(data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, updatetime)

def update_updatetime_all_pub(self, data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, updatetime):
    self.DB.update_updatetime_all_pub(data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, updatetime)

def validate_admin_pub_site_upload_deleted(self, data, Bulk_db, Komli_db, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, common_db_user_name, common_db_password, common_db_port, user):
    self.DB.validate_admin_pub_site_upload_deleted(data, Bulk_db, Komli_db, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, common_db_user_name, common_db_password, common_db_port, user)

def validate_pub_upload(self, data, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port):
    self.DB.validate_pub_upload(data, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port)

def validate_plat_upload(self, data, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, version=1):
    self.DB.validate_plat_upload(data, fraud_db_host, int(fraud_db_port), fraud_db_user_name, fraud_db_password, crawl_db_host, int(crawl_db_port), crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, version)

def update_crawler_v_to_2(self, data, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port):
    self.DB.update_crawler_v_to_2(data, fraud_db_host, int(fraud_db_port), fraud_db_user_name, fraud_db_password, crawl_db_host, int(crawl_db_port), crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port)

def validate_gssb(self, data, db_host, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port):
    self.DB.validate_gssb(data, db_host, int(db_port), db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port)

def validate_pub_pub_site_upload(self, data, Bulk_db, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, Komli_db, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, common_db_user_name, common_db_password, common_db_port, user):
    self.DB.validate_pub_pub_site_upload(data, Bulk_db, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, Komli_db, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, common_db_user_name, common_db_password, common_db_port, user)

def validate_bulk_upload_table(self, fileName, db_host, db_user_name, db_password, db_port):
    df_db = self.DB.get_BulkOps_db_data(fileName, db_host, db_user_name, db_password, int(db_port))
    df_ui = self.acc7.pmccTable("//table[@class='pmcc-table pmcc-fixed-header']", None, None, True)
    df_ui = df_ui.drop(['User'], axis=1)
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop(['Upload Date'], axis=1)
    BuiltIn().log('DB DATAFRAME')
    BuiltIn().log('UI DATAFRAME')
    BuiltIn().log(df_ui)
    self.search_in_df_bulk(df_ui, df_db)
    print('validate_bulk_upload_table completed')

def validate_plat_upload_bulk_upload_table(self, fileName, db_host, db_user_name, db_password, db_port):
    df_db = self.DB.get_BulkOps_db_data(fileName, db_host, db_user_name, db_password, int(db_port))
    df_ui = self.acc7.pmccTable('//iq-bulk-upload-allowlist-domain//table', None, None, True)
    df_ui = df_ui.drop(['User'], axis=1)
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop(['Upload Date'], axis=1)
    BuiltIn().log('DB DATAFRAME')
    BuiltIn().log('UI DATAFRAME')
    BuiltIn().log(df_ui)
    self.search_in_df_bulk(df_ui, df_db)

def validate_pub_upload_bulk_upload_table(self, fileName, db_host, db_user_name, db_password, db_port):
    df_db = self.DB.get_BulkOps_db_data(fileName, db_host, db_user_name, db_password, int(db_port))
    df_ui = self.acc7.pmccTable_pub("//pmcc-scrollable-table//table[@class='pmcc-table']", "//pmcc-scrollable-table//div[@class='header-container has-scroll']//table//thead//th", None, None, True)
    df_ui = df_ui.drop(['User'], axis=1)
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop(['Upload Date'], axis=1)
    BuiltIn().log('DB DATAFRAME')
    BuiltIn().log('UI DATAFRAME')
    BuiltIn().log(df_ui)
    self.search_in_df_bulk(df_ui, df_db)

def validate_pub_site_upload_bulk_upload_table(self, fileName, db_host, db_user_name, db_password, db_port):
    df_db = self.DB.get_BulkOps_db_data(fileName, db_host, db_user_name, db_password, int(db_port))
    df_ui = self.acc7.pmccTable_pub("//pmcc-scrollable-table//table[@class='pmcc-table']", "//pmcc-scrollable-table//div[@class='header-container has-scroll']//table//thead//th", None, None, True)
    df_ui = df_ui.drop(['User'], axis=1)
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop(['Upload Date'], axis=1)
    BuiltIn().log('DB DATAFRAME')
    BuiltIn().log('UI DATAFRAME')
    BuiltIn().log(df_ui)
    self.search_in_df_bulk(df_ui, df_db)

def search_in_df_bulk(self, actual_df, expected_df):
    cols = list(actual_df.columns)
    rowsCount = expected_df.count()[0]
    actual_df_values = actual_df.values
    expected_df_values = expected_df.values
    actual_df_values = actual_df_values.astype('unicode')
    expected_df_values = expected_df_values.astype('unicode')
    actual_df = pd.DataFrame(data=actual_df_values, columns=actual_df.columns)
    expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
    new_df = pd.merge(actual_df, expected_df, on=cols, how='left', indicator='Exist')
    new_df['Exist'] = np.where(new_df.Exist == 'both', True, False)
    print('Merged DF')
    print(new_df)
    resultList = list(new_df['Exist'])
    print(resultList)
    flag = False
    for result in resultList:
        if result:
            print('Expected data found ')
            flag = True
        else:
            print('Expected data Not found ')
    if flag:
        print('all records matched')
    else:
        raise Exception('all records didnt match')

def search_in_df(self, actual_df, expected_df):
    cols = list(actual_df.columns)
    rowsCount = expected_df.count()[0]
    actual_df_values = actual_df.values
    expected_df_values = expected_df.values
    actual_df_values = actual_df_values.astype('unicode')
    expected_df_values = expected_df_values.astype('unicode')
    actual_df = pd.DataFrame(data=actual_df_values, columns=actual_df.columns)
    expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
    new_df = pd.merge(actual_df, expected_df, on=cols, how='left', indicator='Exist')
    new_df['Exist'] = np.where(new_df.Exist == 'both', True, False)
    print('Merged DF')
    print(new_df)
    resultList = list(new_df['Exist'])
    print(resultList)
    flag = True
    for result in resultList:
        if result:
            print('Expected data found ')
        else:
            print('Expected data Not found ')
            flag = False
    if not flag:
        print('all records didnt match')
    else:
        print('all records matched')

def search_in_df_single(self, actual_df, expected_df):
    cols = list(actual_df.columns)
    rowsCount = expected_df.count()[0]
    actual_df_values = actual_df.values
    expected_df_values = expected_df.values
    actual_df_values = actual_df_values.astype('unicode')
    expected_df_values = expected_df_values.astype('unicode')
    actual_df = pd.DataFrame(data=actual_df_values, columns=actual_df.columns)
    expected_df = pd.DataFrame(data=expected_df_values, columns=actual_df.columns)
    print('search_in_df')
    print(actual_df)
    print(expected_df)
    print(actual_df == expected_df)
    found = actual_df == expected_df
    print('found : ' + str(found))
    print(type(found))
    if found:
        print('Expected data found ')
    else:
        raise Exception('Expected data Not found ')

def wait_for_spinner_to_disappear(self, timeout=60):
    """
        Waits for the spinner to disappear
        :return: None
        """
    defaultTimeout = self.s2l.set_selenium_implicit_wait(1)
    spinner_available = BuiltIn().run_keyword_and_return_status('element_should_be_visible', '//pmcc-spinner')
    start_time = time.time()
    while spinner_available and start_time + timeout > time.time():
        spinner_available = BuiltIn().run_keyword_and_return_status('element_should_be_visible', '//pmcc-spinner')
    if spinner_available:
        BuiltIn().fail("pmcc-spinner didn't disappear in {} sec".format(timeout))
    self.s2l.set_selenium_implicit_wait(defaultTimeout)

def populate_data(self, test_data, db_server, db_port, db_user, db_password, komli_db_host, common_db_port, common_db_user_name, common_db_password):
    publisher_allowlist_records = test_data['populate_publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    start = time.time()
    delete_sql = ' delete from  fraud_mgmt.publisher_allowlist where adserving_entity in ('
    insert_sql = ' insert ignore into fraud_mgmt.publisher_allowlist(pub_id,adserving_entity,platform_id,store_id,application_profile_id,crc_64)values'
    publisher_allowlist_records = test_data['populate_publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() != 'none':
        records = publisher_allowlist_records.split('\n')
        for record in records:
            data = record.split(',')
            tld_name = data[1]
            tld_name_tmp = str(tld_name).replace("'", '')
            crc_64 = self.calculate_crc64(tld_name_tmp)
            delete_sql = delete_sql + str(tld_name) + ','
            insert_sql = insert_sql + '(' + str(record) + ",-1,'" + str(crc_64) + "'),"
    delete_sql = delete_sql[:-1]
    delete_sql = delete_sql + ');'
    print(delete_sql)
    mycursor.execute(delete_sql)
    mydb.commit()
    insert_sql = insert_sql[:-1]
    print(insert_sql)
    mycursor.execute(insert_sql)
    mydb.commit()
    end = time.time()
    print('Time taken= ' + str(end - start))
    mydb = mysql.connector.connect(host=str(komli_db_host), user=str(common_db_user_name), passwd=str(common_db_password), port=str(common_db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    publisher_allowlist_records = test_data['populate_publisher_site_tld_records']
    delete_sql = 'delete from  KomliAdServer.publisher_aggregator_site_tld where pub_id=301 and tld_name in ('
    insert_sql = 'insert ignore into KomliAdServer.publisher_aggregator_site_tld (pub_id,site_id,tld_name,adserving_entity,platform_id,deleted,crc_32,application_profile_id)values'
    if str(publisher_allowlist_records).lower().strip() != 'none':
        records = publisher_allowlist_records.split('\n')
        for record in records:
            data = record.split(',')
            crc_32 = data[2]
            delete_sql = delete_sql + str(crc_32) + ','
            insert_sql = insert_sql + '(' + str(record) + ',CRC32(' + str(crc_32) + '),-1),'
    delete_sql = delete_sql[:-1]
    delete_sql = delete_sql + ');'
    print(delete_sql)
    mycursor.execute(delete_sql)
    mydb.commit()
    insert_sql = insert_sql[:-1]
    print(insert_sql)
    mycursor.execute(insert_sql)
    mydb.commit()

def clean_up_allowlist_upload(self, test_data, db_server, db_port, db_user, db_password):
    print('insite clean_up_allowlist_upload...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    print('got this data for cleanup' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('#')
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        sql = 'delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;'
        print(sql)
        mycursor.execute(sql)
        mydb.commit()

def clean_up_allowlist_upload_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password, komli_db_host, common_db_user_name, common_db_password, common_db_port):
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, komli_db_host, common_db_user_name, common_db_password, common_db_port, 'KomliAdServer')
    records = publisher_allowlist_records.split('\n')
    print('records are: ', records)
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append('delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
        else:
            sql_texts.append('delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append('delete from fraud_mgmt.staging_publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
        else:
            sql_texts.append('delete from fraud_mgmt.staging_publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ';')
        else:
            sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ';')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from ads_txt_crawler.ads_txt_domains where tld_name='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from ads_txt_crawler.store_urls where app_bundle_id='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, crawl_db_server, crawl_db_user, crawl_db_password, crawl_db_port, 'ads_txt_crawler')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawk_db_server, hawk_db_user, hawk_db_password, hawk_db_port, 'HawkEye')

def clean_up_pub_allowlist_upload_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, user):
    print('insite clean_up_allowlist_upload...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    print('got this data for cleanup' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    platf = {'Web': '1', 'Mobile Web': '2', 'Mobile App Android': '5', 'Mobile App iOS': '4', 'CTV': '7'}
    storef = {'Roku': '3', 'Other': '999999', '': '0'}
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append('delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' and store_id=' + str(storef[store_id]) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append('delete from fraud_mgmt.staging_publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' and store_id=' + str(storef[store_id]) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' ;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from ads_txt_crawler.ads_txt_domains where tld_name='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from ads_txt_crawler.store_urls where app_bundle_id='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, crawl_db_server, crawl_db_user, crawl_db_password, crawl_db_port, 'ads_txt_crawler')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawkeye_db_server, hawkeye_db_user, hawkeye_db_password, hawkeye_db_port, 'HawkEye')

def clean_up_pub_pub_site_allowlist_upload_new(self, test_data, Komli_db_server, BulkOps_db_server, common_db_port, common_db_user_name, common_db_password, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, user):
    print('insite clean_up_allowlist_upload...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        site_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        sql_texts.append('delete from KomliAdServer.publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id=' + str(site_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, Komli_db_server, common_db_user_name, common_db_password, common_db_port, 'KomliAdServer')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        site_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        sql_texts.append('delete from BulkOpsMgmt.staging_publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id=' + str(site_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, BulkOps_db_server, common_db_user_name, common_db_password, common_db_port, 'BulkOpsMgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' ;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from ads_txt_crawler.ads_txt_domains where tld_name='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from ads_txt_crawler.store_urls where app_bundle_id='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, crawl_db_server, crawl_db_user, crawl_db_password, crawl_db_port, 'ads_txt_crawler')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawkeye_db_server, hawkeye_db_user, hawkeye_db_password, hawkeye_db_port, 'HawkEye')

def clean_up_pub_site_allowlist_upload_new(self, test_data, Komli_db_server, BulkOps_db_server, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, common_db_port, common_db_user_name, common_db_password, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password):
    print('insite clean_up_allowlist_upload...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        adserving_entity = data[2]
        platform_id = data[3]
        store_id = data[4]
        if platform_id in ['1', '2']:
            sql_texts.append('delete from KomliAdServer.publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id=' + str(site_id) + " and adserving_entity='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and application_profile_id=-1;')
        else:
            sql_texts.append('delete from KomliAdServer.publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id=' + str(site_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, Komli_db_server, common_db_user_name, common_db_password, common_db_port, 'KomliAdServer')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        adserving_entity = data[2]
        platform_id = data[3]
        store_id = data[4]
        if platform_id in ['1', '2']:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
        else:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, Komli_db_server, common_db_user_name, common_db_password, common_db_port, 'KomliAdServer')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        adserving_entity = data[2]
        platform_id = data[3]
        store_id = data[4]
        if platform_id in ['1', '2']:
            sql_texts.append('delete from BulkOpsMgmt.staging_publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id=' + str(site_id) + " and adserving_entity='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and application_profile_id=-1;')
        else:
            sql_texts.append('delete from BulkOpsMgmt.staging_publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id=' + str(site_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, BulkOps_db_server, common_db_user_name, common_db_password, common_db_port, 'BulkOpsMgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        adserving_entity = data[2]
        platform_id = data[3]
        store_id = data[4]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from ads_txt_crawler.ads_txt_domains where tld_name='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from ads_txt_crawler.store_urls where app_bundle_id='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, crawl_db_server, crawl_db_user, crawl_db_password, crawl_db_port, 'ads_txt_crawler')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        adserving_entity = data[2]
        platform_id = data[3]
        store_id = data[4]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawk_db_server, hawk_db_user, hawk_db_password, hawk_db_port, 'HawkEye')

def clean_up_plat_allowlist_upload_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password):
    print('insite clean_up_allowlist_upload...!')
    plat_allowlist_records = test_data['platform_allowlist_records']
    if str(plat_allowlist_records).lower().strip() == 'none':
        return
    platf = {'Web': '1', 'Mobile Web': '2', 'Mobile App Android': '5', 'Mobile App iOS': '4', 'CTV': '7'}
    storef = {'Roku': '3', 'tvOS': 4, 'Fire TV': 5, 'LG TV': 6, 'Vizio': 7, 'Samsung': 8, 'Other': '999999', '': '0'}
    records = plat_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append("delete from fraud_mgmt.platform_allowlist where adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' and store_id=' + str(storef[store_id]) + ';')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = plat_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        if store_id == '':
            store_id = 0
        if platform_id in ['Web', 'Mobile Web']:
            sql_texts.append("delete from ads_txt_crawler.ads_txt_domains where tld_name='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from ads_txt_crawler.store_urls where app_bundle_id='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, crawl_db_server, crawl_db_user, crawl_db_password, crawl_db_port, 'ads_txt_crawler')
    records = plat_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        if store_id == '':
            store_id = 0
        if platform_id in ['Web', 'Mobile Web']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawkeye_db_server, hawkeye_db_user, hawkeye_db_password, hawkeye_db_port, 'HawkEye')

def clean_up_gssb(self, test_data, Komli_db_server, db_port, db_user, db_password):
    print('insite clean_up_gssb...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        adserving_entity = data[0]
        platform_id = data[1]
        if platform_id in ['1', '2']:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
        else:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, Komli_db_server, db_user, db_password, db_port, 'KomliAdServer')

def validate_allowlist_upload(self, test_data, test_case, db_server, db_port, db_user, db_password, komli_db_host, activity_db_host, common_db_user_name, common_db_password, common_db_port):
    print('got this as test_case ' + str(test_case))
    publisher_allowlist_records = self.get_data_frame_value(test_data, test_case, 'publisher_allowlist_records')
    print('publisher_allowlist_records= ' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('\n')
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        is_deleted = str(data[4]).strip()
        sql = 'select pub_id from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;'
        print(sql)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        db_result = ''
        if len(result) != 0:
            db_result = result[0][0]
        mydb.commit()
        if str(db_result) == str(pub_id):
            print('publisher_allowlist validation done!')
            self.validate_publisher_aggregater(test_data, test_case, komli_db_host, common_db_port, common_db_user_name, common_db_password)
        elif str(is_deleted) == '1':
            print('publisher_allowlist delete validation done!')
            self.validate_publisher_aggregater(test_data, test_case, komli_db_host, common_db_port, common_db_user_name, common_db_password)
        else:
            raise Exception('publisher_allowlist validation failed')

def validate_allowlist_stats(self, test_data, db_server, db_port, db_user, db_password):
    return
    print('got this as test_case stats ' + str(test_case))
    publisher_allowlist_records = self.get_data_frame_value(test_data, test_case, 'publisher_allowlist_stats')
    print('publisher_allowlist_stats= ' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('\n')
    for record in records:
        data = record.split('#')
        allowlist_type = data[0]
        total_records = data[1]
        processed_records = data[2]
        failed_records = data[3]
        failed_stats = data[4]
        history_lookups = data[5]
        sql = 'select pub_id from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and allowlist_type='" + str(allowlist_type) + "' and total_records= " + str(total_records) + ' and processed_records=' + str(processed_records) + ' and failed_records=' + str(failed_records) + ' and history_lookups=' + str(history_lookups) + ';'
        print(sql)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        db_result = ''
        if len(result) != 0:
            db_result = result[0][0]
        mydb.commit()
        if str(db_result) == str(pub_id):
            print('publisher_allowlist stats validation done!')
        else:
            raise Exception('publisher_allowlist stats validation failed')

def validate_publisher_aggregater(self, test_data, test_case, db_server, db_port, db_user, db_password):
    publisher_allowlist_records = self.get_data_frame_value(test_data, test_case, 'publisher_site_tld_records')
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('\n')
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        tld_name = data[2]
        adserving_entity = data[3]
        platform_id = data[4]
        deleted = data[5]
        sql = 'select pub_id from KomliAdServer.publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id= ' + str(site_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + " and tld_name='" + str(tld_name) + "' and deleted=" + str(deleted) + ' and application_profile_id=-1;'
        print(sql)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        db_result = result[0][0]
        mydb.commit()
        if str(db_result) == str(pub_id):
            print('validate_publisher_aggregater validation done!')
        else:
            raise Exception('validate_publisher_aggregater validation failed')

def calculate_crc64(self, string):
    crc64_tab = [0, 8851949072701294969, 17703898145402589938, 10333669153493130123, 13851072938616403599, 13465927519055396854, 3857338458010461309, 5715195658523061508, 12333367839138578037, 15127763206205961996, 6816212484437830791, 2612226237385041406, 7714676916020922618, 1281407202545942915, 11430391317046123016, 16463076249205199729, 9009731685717012353, 563108230357313272, 9851657908567506291, 17465080730062222346, 13632424968875661582, 14404880506683019383, 5224452474770082812, 3627802401766982277, 15429353832041845236, 12463821128841762957, 2562814405091885830, 6433535930597116543, 1592294032496338811, 7836410910743637506, 16404387395731993993, 11056451039949864176, 18019463371434024706, 9280105458721969787, 1126216460714626544, 8464919223366468745, 4190910634541279629, 4679640014836523252, 14959263154764675967, 13060872525739979270, 5852729821509460343, 3161916214005835790, 11856275032257016709, 16019730051968187132, 10448904949540165624, 16994763621833383553, 7255604803533964554, 2191395843288271987, 9734813498046853251, 18285020776702097914, 8262382231073956465, 608425843627928328, 5125628810183771660, 4465764294926438261, 12867071861194233086, 14432195567501024647, 3184588064992677622, 6262709589572306831, 15672821821487275012, 11770576130456212861, 17008134862606432377, 10867599606483677440, 1853769023980628619, 7161174014982448114, 16103423924954344815, 11935289383220651030, 3083341959784644509, 5769757520242456292, 2252432921429253088, 7321251034957484697, 16929838446732937490, 10388307452745547883, 8381821269082559258, 1047727658635319907, 9359280029673046504, 18102965619612993681, 13000435797616977301, 14894146905688698092, 4745161141923116903, 4252033715651608094, 11705459643018920686, 15612384854998895511, 6323832428011671580, 3250108949404244325, 7082685524280996961, 1770671381070249240, 10951102161764411027, 17087309740654948330, 674072313427442843, 8323419547594995170, 18224423522563763817, 9669888565606754064, 14511209607067929108, 12950765422787986285, 4382791686576543974, 5047054248884015519, 2696289253709771373, 6895947823530343188, 15049839570318909599, 12250835051042597350, 16524764462147912930, 11496477575961038235, 1216851687255856656, 7654800921679748969, 10251257620367543320, 17625884659327141217, 8931528589852876522, 84259039178430355, 5655163293556783767, 3792978414742418414, 13532134484260726885, 13912670750543257884, 6369176129985355244, 2502782282785952917, 12525419179144613662, 15495561035627234919, 10978437246791527267, 16321975555527844378, 7920669638525335953, 1671873238255513832, 17531166746306175897, 9913345878835194592, 503231997654823275, 8945175932061546514, 3707538047961257238, 5308515798192249967, 14322348029964896228, 13554501644362141341, 10785157014839085493, 17254666630495879372, 6925536469308201799, 1928669229005230654, 6166683919569289018, 3408106242218915395, 11539515040484912584, 15779741191858611377, 4504865842858506176, 4925828954283753145, 14642502069914969394, 12820884771576065099, 18355716529793696079, 9540007361421969462, 796147016248169405, 8202193697865996996, 16763642538165118516, 10555343349626187597, 2095455317270639814, 7479631577382337983, 2926364910754730171, 5928137516128508354, 15937228569359352393, 12102324735718361904, 4867406749023426625, 4131191115536978232, 13131477498808912563, 14763945261529023434, 9490322283846233806, 17972763431062038455, 8504067431303216188, 926884511990314309, 8051711962477172407, 1541670979892322254, 11100683476643087429, 16201132341218348348, 12647664856023343160, 15374718365700663617, 6500217898808488650, 2372580570961558451, 14165371048561993922, 13712881572587659707, 3541342762140498480, 5475551080882205513, 337036156713721421, 9112211761281881908, 17374189211922025663, 10071726351451997638, 1348144626854885686, 7524919785159454799, 16646839095189990340, 11375251796044276413, 15171913658969673657, 12129609824107054784, 2827581646778391883, 6766067242130363442, 13374985906044110659, 14070668113165684282, 5489218623395763633, 3960334819262667976, 8765583373153087948, 251615998827411637, 10094108497768031038, 17783882574922426951, 5392578507419542746, 3462768234654100899, 13791895647060686376, 14249064643987996497, 10011129131143811669, 17309264314385947436, 9177858264896848039, 398073508124084702, 16284634862666717871, 11179858319785628630, 1463182455377365085, 7968614284679676196, 2433703374511713312, 6565738749404456281, 15309601843359497938, 12587227855704700843, 4025855981238586203, 5550341738321543714, 14010231419946703273, 13309869690798280912, 17863057179705753044, 10177610780853122221, 168518078356860710, 8687094605961012831, 11310326587113567534, 16586241563491499095, 7585956829484836828, 1413790823389195941, 6687492953022055329, 2744609311697881816, 12213303662187237715, 15250927976100943914, 12738352259970710488, 14564578711588090529, 5005564565571905834, 4588929132448424019, 8142317431333358935, 731591227688682542, 9606093343850471333, 18417404465172059868, 2012927990619293101, 7005115709973351636, 17176652871151048543, 10702745209522052646, 15841339277050671906, 11605722277885901403, 3343746476511027664, 6106651831093618857, 14830152191845028953, 13193075276920315168, 4071158715666679467, 4803046671925235666, 1006463995309646550, 8588326435575524271, 17890351864123093028, 9412308762883553629, 7415076095922514476, 2035579357833339733, 10617031596384499934, 16829728831969243559, 12024401134718426275, 15854695815076877786, 6012200567359213137, 3006100283679606568]
    string = str(string)
    crc = 0
    for i in range(0, len(string)):
        crc = crc64_tab[crc % 256 ^ ord(string[i])] ^ crc >> 8
    print("CRC generated for string : '%s' is : %d" % (string, crc))
    return crc

def global_channel_partner_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['gcpb_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values'
    delete_sql = 'delete from KomliAdServer.global_channel_partner_block_list where '
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        domain = req_data[0]
        platform = req_data[1]
        action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from KomliAdServer.global_channel_partner_block_list where domain='" + domain + "';")
            sql_texts_add.append("insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values('" + domain + "'," + platform + ');')
        elif action == 'remove':
            self.gcpb_remove(domain, platform, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'KomliAdServer')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'KomliAdServer')

def gcpb_add(self, domain, platform, db_server, db_port, db_user, db_password):
    self.gcpb_remove(domain, platform, db_server, db_port, db_user, db_password)
    print('adding domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values('" + domain + "'," + platform + ');'
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def gcpb_remove(self, domain, platform, db_server, db_port, db_user, db_password):
    print('removing domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "delete from KomliAdServer.global_channel_partner_block_list where domain='" + domain + "';"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def global_publisher_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['gssb_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id)values'
    delete_sql = 'delete from KomliAdServer.global_supply_side_blocklist where '
    print('inside GPBL filter')
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    for line in req_lines:
        req_data = line.split(',')
        domain = req_data[0]
        platform = req_data[1]
        action = req_data[2].lower()
        if action == 'add':
            print('adding')
            self.gssb_add(domain, platform, db_server, db_port, db_user, db_password)
        elif action == 'remove':
            self.gssb_remove(domain, platform, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(domain))

def global_publisher_blocklist_filter_new(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['gssb_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id)values'
    delete_sql = 'delete from KomliAdServer.global_supply_side_blocklist where '
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        domain = req_data[0]
        platform = req_data[1]
        if len(req_data) == 4:
            store_id = req_data[2]
            action = req_data[3].lower()
        else:
            store_id = 0
            action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + domain + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append("insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id,reason)values('" + domain + "'," + platform + ',' + str(store_id) + ",'automation');")
        elif action == 'remove':
            self.gssb_remove_new(domain, platform, store_id, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'KomliAdServer')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'KomliAdServer')

def hawkeye_app_details_add_del(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['hawkeye_app_details']
    if str(request_line).lower().strip() == 'none':
        return
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        canonical_id = req_data[0]
        platform = req_data[1]
        if len(req_data) == 4:
            store_id = req_data[2]
            action = req_data[3].lower()
        else:
            store_id = 0
            action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from HawkEye.app_details where canonical_id='" + canonical_id + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append("insert ignore HawkEye.app_details(canonical_id,platform_id,store_id,source) values('" + canonical_id + "'," + platform + ',' + str(store_id) + ",'automation');")
        elif action == 'remove':
            self.hawkeye_app_details_remove_new(canonical_id, platform, store_id, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(canonical_id))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'HawkEye')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'HawkEye')

def publisher_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['pub_block_filter']
    if str(request_line).lower().strip() == 'none':
        return
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        pubid = req_data[0]
        domain = req_data[1]
        platform = req_data[2]
        if len(req_data) == 5:
            store_id = req_data[3]
            action = req_data[4].lower()
        else:
            store_id = 0
            action = req_data[3].lower()
        if action == 'add':
            sql_texts_del.append("delete from fraud_mgmt.pub_blocklist where domain='" + domain + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append('insert ignore fraud_mgmt.pub_blocklist(pub_id,domain,platform_id,store_id)values(' + pubid + ",'" + domain + "'," + platform + ',' + str(store_id) + ');')
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'fraud_mgmt')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'fraud_mgmt')

def platform_allowlist_filter_new(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['plat_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore fraud_mgmt.platform_allowlist(adserving_entity,platform_id,store_id)values'
    delete_sql = 'delete from fraud_mgmt.platform_allowlist where '
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        domain = req_data[0]
        platform = req_data[1]
        if len(req_data) == 4:
            store_id = req_data[2]
            action = req_data[3].lower()
        else:
            store_id = 0
            action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from fraud_mgmt.platform_allowlist where adserving_entity='" + domain + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append("insert ignore fraud_mgmt.platform_allowlist(adserving_entity,platform_id,store_id)values('" + domain + "'," + platform + ',' + str(store_id) + ');')
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'fraud_mgmt')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'fraud_mgmt')

def gssb_add(self, domain, platform, db_server, db_port, db_user, db_password):
    self.gssb_remove(domain, platform, db_server, db_port, db_user, db_password)
    print('adding domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,reason)values('" + domain + "'," + platform + ",'automation');"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def gssb_remove(self, domain, platform, db_server, db_port, db_user, db_password):
    print('removing domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "delete from KomliAdServer.global_supply_side_blocklist where domain='" + domain + "';"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def gssb_add_new(self, domain, platform, store_id, db_server, db_port, db_user, db_password):
    self.gssb_remove_new(domain, platform, store_id, db_server, db_port, db_user, db_password)
    print('adding domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id,reason)values('" + domain + "'," + platform + ',' + str(store_id) + ",'automation');"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def gssb_remove_new(self, domain, platform, store_id, db_server, db_port, db_user, db_password):
    print('removing domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "delete from KomliAdServer.global_supply_side_blocklist where domain='" + domain + "' and store_id=" + str(store_id) + ';'
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

def hawkeye_app_details_remove_new(self, canonical_id, platform, store_id, db_server, db_port, db_user, db_password):
    print('removing domain from hawkeye db - app details table')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='HawkEye')
    mycursor = mydb.cursor()
    sql = "delete from HawkEye.app_details where canonical_id='" + canonical_id + "'and platform_id='" + platform + "' and store_id=" + str(store_id) + ';'
    print(sql)
    mycursor.execute(sql)
    mydb.commit()

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

def get_fileid_from_name(self, db_server, db_port, db_user, db_password):
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), port=str(db_port), passwd=str(db_password), database='ActivityLog')
    mycursor = mydb.cursor()
    sql = "select id  from bulk_operations where  file_name ='" + str(self.activity_file_name) + "'; "
    print(sql)
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if isinstance(data, tuple):
        for x in data:
            return x
        print('sleeping')
        mydb.commit()
    raise Exception('Bulk file not found')

def heimdall_cache_refresh(self, api_endpoint, token):
    url = str(api_endpoint) + '/heimdall/cache-refresh'
    payload = ''
    headers = {'Content-Type': 'application/json', 'pubtoken': str(token), 'cache-control': 'no-cache', 'Postman-Token': '604f3d8a-f148-49e1-ba8d-e79416b77e74'}
    response = requests.request('GET', url, data=payload, headers=headers)
    print(response.text)

def returndataframe(self, csvPath, sheetName):
    self.excelDF = self.excelTableToDataFrame(csvPath, sheetName)
    return self.excelDF.copy().to_dict()

def get_data_frame_value(self, data_frame, test='', column=''):
    column_position = '0'
    header_list = data_frame['Test Cases/Test Data']
    print('header_list=' + str(header_list))
    for (i, j) in header_list.items():
        if str(j) == column:
            column_position = i
    test_cases = data_frame
    print('Checking')
    print(test)
    print(column)
    for (v, k) in test_cases.items():
        print('checking with')
        print(str(v).lower())
        if str(v).lower() == str(str(test).lower()):
            key_found = v
            print('key_found: ' + str(k))
            print(data_frame[key_found][int(column_position)])
            return data_frame[key_found][int(column_position)]
        else:
            print('key not found')

def excelTableToDataFrame(self, excelPath, sheetName):
    df = pd.read_excel(open(excelPath, 'rb'), sheet_name=sheetName)
    return df

def update_spoofer_response_file(self, spoofer_server_url, file_name, response_txt):
    print('spoof started')
    url = 'http://' + spoofer_server_url + '/updatespoofdata'
    payload = response_txt
    headers = {'file_name': file_name}
    response = requests.request('POST', url, data=payload, headers=headers)
    print('completed')

def heimdall_cache_refresh_app_onboarding_check(self, uri, token, value):
    import requests
    import json
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'allowlisting.ctv.app.onboarding.check': '{}'.format(value)})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh with token ' + str(token))
    else:
        print('heimdall_cache_refresh completed..!')

def heimdall_cache_refresh_canonical_regex(self, uri, token):
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    print(url)
    payload = json.dumps({'canonical.regex.validation.3': '^[0-9]+$', 'canonical.regex.validation.4': '^[0-9]+$', 'canonical.regex.validation.5': '^[a-zA-Z0-9]+$', 'canonical.regex.validation.6': '^[0-9]+$', 'canonical.regex.validation.7': '^[a-zA-Z.]+$', 'canonical.regex.validation.8': '^[a-zA-Z0-9]+$', 'canonical.regex.validation.9': '^[a-zA-Z.]+$'})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_app_Config_cache_refresh with token ' + str(token))
    else:
        print('heimdall_app_Config_cache_refresh completed..!')

def heimdall_cache_refresh_canonical_supported_store_ids(self, uri, token):
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'canonical.support.valid.store.ids': '3#4#5#6#7#8#999999'})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh_canonical_supported_store_ids with token ' + str(token))
    else:
        print('heimdall_cache_refresh_canonical_supported_store_ids completed..!')

def heimdall_cache_refresh_lookup_storeIds(self, uri, token, value):
    import requests
    import json
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'allowlisting.ctv.ratingserver.lookup.storeIds': '{}'.format(value), 'resttemplate.retry.delay.seconds': 1, 'resttemplate.retry.max.attempt': 1})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh with token ' + str(token))
    else:
        print('heimdall_cache_refresh completed..!')

def heimdall_cache_refresh_ratingserver_na_action(self, uri, token, value):
    import requests
    import json
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'allowlisting.ctv.ratingserver.na.action': '{}'.format(value)})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh with token ' + str(token))
    else:
        print('heimdall_cache_refresh completed..!')

def heimdall_cache_refresh_ratingserver_other_action(self, uri, token, value):
    import requests
    import json
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'allowlisting.ctv.ratingserver.other.action': '{}'.format(value)})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh with token ' + str(token))
    else:
        print('heimdall_cache_refresh completed..!')

def heimdall_cache_refresh_ratingserver_other_action(self, uri, token, value):
    import requests
    import json
    url = 'https://{}/heimdall/appconfig/refresh'.format(uri)
    payload = json.dumps({'allowlisting.ctv.ratingserver.other.action': '{}'.format(value)})
    headers = {'pubtoken': '{}'.format(token), 'Content-Type': 'application/json'}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 200:
        print(response.status_code)
        raise Exception('called heimdall_cache_refresh with token ' + str(token))
    else:
        print('heimdall_cache_refresh completed..!')

def topLevelAdContainer_updateCTVApps(self, uri, token):
    import requests
    import json
    url = 'https://{}/heimdall/topLevelAdContainer/updateCTVApps?pubIdsLimit=100&recordLimit=5000'.format(uri)
    payload = {}
    headers = {'pubtoken': '{}'.format(token)}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 202:
        print(response.status_code)
        raise Exception('failed topLevelAdContainer_updateCTVApps with token ' + str(token))
    else:
        print('topLevelAdContainer_updateCTVApps completed..!')

def reProcess_pub_site(self, uri, token):
    import requests
    import json
    url = 'https://ci-va2qa-mgmt.pubmatic.com/heimdall/topLevelAdContainer/reProcess?noOfDays=1'
    payload = {}
    headers = {'pubtoken': '{}'.format(token)}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 202:
        print(response.status_code)
        raise Exception('failed reProcess_pub_site with token ' + str(token))
    else:
        print('reProcess_pub_site completed..!')
    import time
    time.sleep(60)

def reProcess_pub(self, uri, token):
    import requests
    import json
    url = 'https://ci-va2qa-mgmt.pubmatic.com/heimdall/publisherAllowlist/reProcess?noOfDays=1'
    payload = {}
    headers = {'pubtoken': '{}'.format(token)}
    response = requests.request('POST', url, headers=headers, data=payload)
    print(response.text)
    if response.status_code != 202:
        print(response.status_code)
        raise Exception('failed reProcess_pub with token ' + str(token))
    else:
        print('reProcess_pub completed..!')

def add_to_gssb(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user):
    self.global_publisher_blocklist_filter_new(data, Komli_db, db_port, db_user_name, db_password)

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

def insert_app_details(self, test_data, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password):
    self.DB.insert_app_details(test_data, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password)

def loginAsPublisher(self, URI, publisherLoginID, publisherPassword, selectAccount=None, isSecureLogin=False, gitLoginRequired=False, gitUserName=None, gitPassword=None):
    """
        Login to a publisher page
        :param URI: URL without http:// ex: appbeta.pubmatic.com
        :param publisherLoginID: publisher Login ID
        :param publisherPassword: publisher Login password
        :param selectAccount: string value of account to be selected from singleselect component
        :param isSecureLogin: bool True/False, true if https required, false if http
        :param gitLoginRequired bool True/False
        :param gitUserName: git login username
        :param gitPassword: git login password
        :return: None
        """
    default_timeout = self.s2l.set_selenium_implicit_wait(2)
    if gitLoginRequired:
        if gitUserName is not None and gitPassword is not None:
            self.gitLogin(gitUserName, gitPassword)
        else:
            BuiltIn().fail('git username or password required to login to git')
    if isSecureLogin:
        URL = 'https://'
    else:
        URL = 'http://'
    URL = URL + URI + '/login/publisher'
    usernameXpath = 'id=okta-signin-username'
    passwordXpath = 'id=okta-signin-password'
    loginButtonXpath = 'id=okta-signin-submit'
    dashBoardXpath = "//h1[contains(@class, 'pmcc-page-tite')]"
    self.s2l.maximize_browser_window()
    BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'click_element', usernameXpath)
    self.s2l.input_text(usernameXpath, publisherLoginID)
    self.s2l.input_text(passwordXpath, publisherPassword)
    self.s2l.click_element(loginButtonXpath)
    BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'element_should_contain', "//div[@data-pm-id='email']", 'user_302@pubmatic.com')
    if selectAccount is not None:
        self.selectAccount(selectAccount)

def selectAccount(self, selectAccountValue):
    """
        selects an account after publisher/admin login
        :param selectAccountValue: string account value to be selected from singleselect
        :return: None
        """
    selectAccountSingleSelectXpath = "//pmcc-singleselect[@data-pm-id='accounts-dropdown']"
    accountSelectInputBoxXpath = "//*[@data-pm-id='search-input']//input"
    accountSelectXpath = "//*[@class='pmcc-table pmcc-table-borderless']//tbody//tr//td//span[text()='{}']".format(selectAccountValue)
    loginButtonXpath = "//button[@data-pm-id='continue-btn']"
    BuiltIn().wait_until_keyword_succeeds('30 sec', '2 sec', 'page_should_contain_element', selectAccountSingleSelectXpath)
    self.s2l.click_element(selectAccountSingleSelectXpath)
    BuiltIn().wait_until_keyword_succeeds('10 sec', '2 sec', 'page_should_contain_element', accountSelectInputBoxXpath)
    self.s2l.input_text(accountSelectInputBoxXpath, selectAccountValue)
    BuiltIn().wait_until_keyword_succeeds('20 sec', '2 sec', 'page_should_contain_element', accountSelectXpath)
    BuiltIn().wait_until_keyword_succeeds('10 sec', '2 sec', 'click_element', accountSelectXpath)
    BuiltIn().wait_until_keyword_succeeds('60 sec', '2 sec', 'click_element', loginButtonXpath)

def infra_upload(self, uri, post_api, file_path):
    url = f'https://{uri}/infrastructure/bulkOperations?mode=upload&resourceUrl={post_api}?entityId=0'
    payload = {}
    headers = {'PubToken': 'token337'}
    with open(file_path, 'rb') as f:
        data = f.read()
    print(data)
    files = {'file': open(file_path, 'rb')}
    print(url)
    print(headers)
    print(payload)
    print(files)
    response = requests.request('POST', url, headers=headers, data=payload, files=files)
    code = response.status_code
    print(code)
    if code == 201:
        import time
        if '/heimdall/publisherWhitelist' in url:
            print('sleeping for 40 sec')
            time.sleep(40)
        elif 'topLevelAdContainer' in url:
            print('sleeping for 40 sec')
            time.sleep(40)
        else:
            print('sleeping for 20 sec')
            time.sleep(20)
    else:
        assert response.status_code == 201

def infra_upload1(self, uri, post_api, file_path):
    url = f'https://{uri}/infrastructure/bulkOperations?{post_api}'
    payload = {}
    headers = {'PubToken': 'token337'}
    files = {'file': open(file_path, 'rb')}
    print(url)
    response = requests.request('POST', url, headers=headers, data=payload, files=files)
    code = response.status_code
    print(code)
    if code == 201:
        import time
        if '/heimdall/publisherWhitelist' in url:
            print('sleeping for 40 sec')
            time.sleep(40)
        elif 'topLevelAdContainer' in url:
            print('sleeping for 40 sec')
            time.sleep(40)
        elif 'publisherAllowlist' in url:
            print('sleeping for 90 sec')
            time.sleep(120)
        else:
            print('sleeping for 20 sec')
            time.sleep(20)

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

def validate_onboard_canonical_flag_in_db(self, pub_id, flag, fraud_db_host, user_name, password, port):
    mydb = mysql.connector.connect(host=str(fraud_db_host), user=str(user_name), port=str(port), passwd=str(password), database=str('fraud_mgmt'))
    query = f'select onboarding_canonical from publisher_iq_settings where pub_id={pub_id} and onboarding_canonical={flag}'
    mycursor = mydb.cursor()
    print(query)
    mycursor.execute(query)
    result = mycursor.fetchone()
    print(result)
    if result is None:
        assert flag != flag

