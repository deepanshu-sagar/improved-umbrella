def global_channel_partner_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['gcpb_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values'
    delete_sql = 'delete from KomliAdServer.global_channel_partner_block_list where '
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
        action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from KomliAdServer.global_channel_partner_block_list where domain='" + domain + "';")
            sql_texts_add.append("insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values('" + domain + "'," + platform + ');')
        elif action == 'remove':
            self.gcpb_remove(domain, platform, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(domain))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'KomliAdServer')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'KomliAdServer')