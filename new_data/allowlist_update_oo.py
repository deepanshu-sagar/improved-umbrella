def update_oo(self, db_host, db_user_name, db_password, db_port, user, value):
    self.DB.update_oo(db_host, db_user_name, db_password, int(db_port), user, value)