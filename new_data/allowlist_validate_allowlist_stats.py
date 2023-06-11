def validate_allowlist_stats(self, test_data, db_server, db_port, db_user, db_password):
    return
    print('got this as test_case stats ' + str(test_case))
    publisher_allowlist_records = self.get_data_frame_value(test_data, test_case, 'publisher_allowlist_stats')
    print('publisher_allowlist_stats= ' + str(publisher_allowlist_records))
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='fraud_mgmt')
    mycursor = mydb.cursor()
    records = publisher_allowlist_records.split('\n')
    for record in records:
        data = record.split('#')
        allowlist_type = data[0]
        total_records = data[1]
        processed_records = data[2]
        failed_records = data[3]
        failed_stats = data[4]
        history_lookups = data[5]
        sql = 'select pub_id from fraud_mgmt.publisher_allowlist where pub_id=' + str(pub_id) + " and allowlist_type='" + str(allowlist_type) + "' and total_records= " + str(total_records) + ' and processed_records=' + str(processed_records) + ' and failed_records=' + str(failed_records) + ' and history_lookups=' + str(history_lookups) + ';'
        print(sql)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        db_result = ''
        if len(result) != 0:
            db_result = result[0][0]
        mydb.commit()
        if str(db_result) == str(pub_id):
            print('publisher_allowlist stats validation done!')
        else:
            raise Exception('publisher_allowlist stats validation failed')