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