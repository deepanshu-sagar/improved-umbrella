def clean_up_allowlist_upload_new(self, test_data, fraud_db_server, fraud_db_port, fraud_db_user, fraud_db_password, crawl_db_server, crawl_db_port, crawl_db_user, crawl_db_password, hawk_db_server, hawk_db_port, hawk_db_user, hawk_db_password, komli_db_host, common_db_user_name, common_db_password, common_db_port):
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, komli_db_host, common_db_user_name, common_db_password, common_db_port, 'KomliAdServer')
    records = publisher_allowlist_records.split('\n')
    print('records are: ', records)
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append('delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
        else:
            sql_texts.append('delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append('delete from fraud_mgmt.staging_publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
        else:
            sql_texts.append('delete from fraud_mgmt.staging_publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity).lower() + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ';')
        else:
            sql_texts.append("delete from fraud_mgmt.ad_container_result_history_lookup where ad_container='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ';')
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, fraud_db_server, fraud_db_user, fraud_db_password, fraud_db_port, 'fraud_mgmt')
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
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
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        if store_id == '':
            store_id = 0
        if platform_id in ['1', '2']:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity).lower() + "';")
        else:
            sql_texts.append("delete from HawkEye.category_fetch_ad_container where ad_container='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, hawk_db_server, hawk_db_user, hawk_db_password, hawk_db_port, 'HawkEye')