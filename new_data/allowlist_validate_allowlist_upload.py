def validate_allowlist_upload(self, test_data, test_case, db_server, db_port, db_user, db_password, komli_db_host, activity_db_host, common_db_user_name, common_db_password, common_db_port):
    print('got this as test_case ' + str(test_case))
    publisher_allowlist_records = self.get_data_frame_value(test_data, test_case, 'publisher_allowlist_records')
    print('publisher_allowlist_records= ' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('\n')
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        is_deleted = str(data[4]).strip()
        sql = 'select pub_id from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;'
        print(sql)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        db_result = ''
        if len(result) != 0:
            db_result = result[0][0]
        mydb.commit()
        if str(db_result) == str(pub_id):
            print('publisher_allowlist validation done!')
            self.validate_publisher_aggregater(test_data, test_case, komli_db_host, common_db_port, common_db_user_name, common_db_password)
        elif str(is_deleted) == '1':
            print('publisher_allowlist delete validation done!')
            self.validate_publisher_aggregater(test_data, test_case, komli_db_host, common_db_port, common_db_user_name, common_db_password)
        else:
            raise Exception('publisher_allowlist validation failed')