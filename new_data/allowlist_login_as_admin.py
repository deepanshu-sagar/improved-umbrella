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