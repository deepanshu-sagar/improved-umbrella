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