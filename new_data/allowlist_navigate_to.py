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