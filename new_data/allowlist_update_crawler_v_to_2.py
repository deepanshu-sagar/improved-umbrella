def update_crawler_v_to_2(self, data, fraud_db_host, fraud_db_port, fraud_db_user_name, fraud_db_password, crawl_db_host, crawl_db_port, crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port):
    self.DB.update_crawler_v_to_2(data, fraud_db_host, int(fraud_db_port), fraud_db_user_name, fraud_db_password, crawl_db_host, int(crawl_db_port), crawl_db_user_name, crawl_db_password, hawkeye_db_user, hawkeye_db_password, hawkeye_db_host, hawkeye_port)