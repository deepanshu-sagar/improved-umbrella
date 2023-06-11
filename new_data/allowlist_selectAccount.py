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