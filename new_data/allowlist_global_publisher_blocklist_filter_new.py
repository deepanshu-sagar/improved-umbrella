def global_publisher_blocklist_filter_new(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['gssb_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id)values'
    delete_sql = 'delete from KomliAdServer.global_supply_side_blocklist where '
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
            sql_texts_del.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + domain + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append("insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id,reason)values('" + domain + "'," + platform + ',' + str(store_id) + ",'automation');")
        elif action == 'remove':
            self.gssb_remove_new(domain, platform, store_id, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'KomliAdServer')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'KomliAdServer')