def clean_up_allowlist_upload(self, test_data, db_server, db_port, db_user, db_password):
    print('insite clean_up_allowlist_upload...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    print('got this data for cleanup' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('#')
    for record in records:
        data = record.split(',')
        pub_id = data[0]
        adserving_entity = data[1]
        platform_id = data[2]
        store_id = data[3]
        sql = 'delete from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and adserving_entity='" + str(adserving_entity) + "' and platform_id= " + str(platform_id) + ' and store_id=' + str(store_id) + ' and application_profile_id=-1;'
        print(sql)
        mycursor.execute(sql)
        mydb.commit()