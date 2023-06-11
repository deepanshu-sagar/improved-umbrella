def validate_publisher_aggregater(self, test_data, test_case, db_server, db_port, db_user, db_password):
    publisher_allowlist_records = self.get_data_frame_value(test_data, test_case, 'publisher_site_tld_records')
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('\n')
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        site_id = data[1]
        tld_name = data[2]
        adserving_entity = data[3]
        platform_id = data[4]
        deleted = data[5]
        sql = 'select pub_id from KomliAdServer.publisher_aggregator_site_tld where pub_id=' + str(pub_id) + ' and site_id= ' + str(site_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + " and tld_name='" + str(tld_name) + "' and deleted=" + str(deleted) + ' and application_profile_id=-1;'
        print(sql)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        db_result = result[0][0]
        mydb.commit()
        if str(db_result) == str(pub_id):
            print('validate_publisher_aggregater validation done!')
        else:
            raise Exception('validate_publisher_aggregater validation failed')