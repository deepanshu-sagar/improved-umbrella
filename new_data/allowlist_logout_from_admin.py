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