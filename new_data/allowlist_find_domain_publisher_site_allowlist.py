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