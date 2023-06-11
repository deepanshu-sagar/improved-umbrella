def populate_data(self, test_data, db_server, db_port, db_user, db_password, komli_db_host, common_db_port, common_db_user_name, common_db_password):
    publisher_allowlist_records = test_data['populate_publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    start = time.time()
    delete_sql = ' delete from  fraud_mgmt.publisher_allowlist where adserving_entity in ('
    insert_sql = ' insert ignore into fraud_mgmt.publisher_allowlist(pub_id,adserving_entity,platform_id,store_id,application_profile_id,crc_64)values'
    publisher_allowlist_records = test_data['populate_publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() != 'none':
        records = publisher_allowlist_records.split('\n')
        for record in records:
            data = record.split(',')
            tld_name = data[1]
            tld_name_tmp = str(tld_name).replace("'", '')
            crc_64 = self.calculate_crc64(tld_name_tmp)
            delete_sql = delete_sql + str(tld_name) + ','
            insert_sql = insert_sql + '(' + str(record) + ",-1,'" + str(crc_64) + "'),"
    delete_sql = delete_sql[:-1]
    delete_sql = delete_sql + ');'
    print(delete_sql)
    mycursor.execute(delete_sql)
    mydb.commit()
    insert_sql = insert_sql[:-1]
    print(insert_sql)
    mycursor.execute(insert_sql)
    mydb.commit()
    end = time.time()
    print('Time taken= ' + str(end - start))
    mydb = mysql.connector.connect(host=str(komli_db_host), user=str(common_db_user_name), passwd=str(common_db_password), port=str(common_db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    publisher_allowlist_records = test_data['populate_publisher_site_tld_records']
    delete_sql = 'delete from  KomliAdServer.publisher_aggregator_site_tld where pub_id=301 and tld_name in ('
    insert_sql = 'insert ignore into KomliAdServer.publisher_aggregator_site_tld (pub_id,site_id,tld_name,adserving_entity,platform_id,deleted,crc_32,application_profile_id)values'
    if str(publisher_allowlist_records).lower().strip() != 'none':
        records = publisher_allowlist_records.split('\n')
        for record in records:
            data = record.split(',')
            crc_32 = data[2]
            delete_sql = delete_sql + str(crc_32) + ','
            insert_sql = insert_sql + '(' + str(record) + ',CRC32(' + str(crc_32) + '),-1),'
    delete_sql = delete_sql[:-1]
    delete_sql = delete_sql + ');'
    print(delete_sql)
    mycursor.execute(delete_sql)
    mydb.commit()
    insert_sql = insert_sql[:-1]
    print(insert_sql)
    mycursor.execute(insert_sql)
    mydb.commit()