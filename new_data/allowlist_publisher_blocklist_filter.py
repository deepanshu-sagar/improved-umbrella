def publisher_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['pub_block_filter']
    if str(request_line).lower().strip() == 'none':
        return
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    sql_texts_del = []
    sql_texts_add = []
    for line in req_lines:
        req_data = line.split(',')
        pubid = req_data[0]
        domain = req_data[1]
        platform = req_data[2]
        if len(req_data) == 5:
            store_id = req_data[3]
            action = req_data[4].lower()
        else:
            store_id = 0
            action = req_data[3].lower()
        if action == 'add':
            sql_texts_del.append("delete from fraud_mgmt.pub_blocklist where domain='" + domain + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append('insert ignore fraud_mgmt.pub_blocklist(pub_id,domain,platform_id,store_id)values(' + pubid + ",'" + domain + "'," + platform + ',' + str(store_id) + ');')
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'fraud_mgmt')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'fraud_mgmt')