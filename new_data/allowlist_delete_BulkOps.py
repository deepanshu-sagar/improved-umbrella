def delete_BulkOps(self, fileName, db_host, db_user_name, db_password, db_port):
    self.DB.delete_BulkOps_db_data(fileName, db_host, db_user_name, db_password, int(db_port))