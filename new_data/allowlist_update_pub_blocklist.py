def update_pub_blocklist(self, db_host, db_user_name, db_password, db_port, user, value):
    self.DB.update_pub_blocklist(db_host, db_user_name, db_password, int(db_port), user, value)