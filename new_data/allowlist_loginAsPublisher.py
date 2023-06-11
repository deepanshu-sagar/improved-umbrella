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