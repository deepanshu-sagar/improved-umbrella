def clean_up_pub_allowlist_upload_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawkeye_db_server, hawkeye_db_port, hawkeye_db_user, hawkeye_db_password, user):
    print('insite clean_up_allowlist_upload...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    print('got this data for cleanup' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    platf = {'Web': '1', 'Mobile Web': '2', 'Mobile App Android': '5', 'Mobile App iOS': '4', 'CTV': '7'}
    storef = {'Roku': '3', 'Other': '999999', '': '0'}
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append('delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' and store_id=' + str(storef[store_id]) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append('delete from fraud_mgmt.staging_publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' and store_id=' + str(storef[store_id]) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity) + "' and platform_id= " + str(platf[platform_id]) + ' ;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from ads_txt_crawler.ads_txt_domains where tld_name='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from ads_txt_crawler.store_urls where app_bundle_id='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, crawl_db_server, crawl_db_user, crawl_db_password, crawl_db_port, 'ads_txt_crawler')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = user
        adserving_entity = data[0]
        platform_id = data[1]
        store_id = data[2]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawkeye_db_server, hawkeye_db_user, hawkeye_db_password, hawkeye_db_port, 'HawkEye')