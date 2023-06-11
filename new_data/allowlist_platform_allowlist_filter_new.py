def platform_allowlist_filter_new(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['plat_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore fraud_mgmt.platform_allowlist(adserving_entity,platform_id,store_id)values'
    delete_sql = 'delete from fraud_mgmt.platform_allowlist where '
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        domain = req_data[0]
        platform = req_data[1]
        if len(req_data) == 4:
            store_id = req_data[2]
            action = req_data[3].lower()
        else:
            store_id = 0
            action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from fraud_mgmt.platform_allowlist where adserving_entity='" + domain + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append("insert ignore fraud_mgmt.platform_allowlist(adserving_entity,platform_id,store_id)values('" + domain + "'," + platform + ',' + str(store_id) + ');')
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'fraud_mgmt')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'fraud_mgmt')