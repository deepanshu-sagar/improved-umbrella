def add_to_gssb(self, data, db_host, Bulk_db, Komli_db, db_port, db_user_name, db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port, user):
    self.global_publisher_blocklist_filter_new(data, Komli_db, db_port, db_user_name, db_password)