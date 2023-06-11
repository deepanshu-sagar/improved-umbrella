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