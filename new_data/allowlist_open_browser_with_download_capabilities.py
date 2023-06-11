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