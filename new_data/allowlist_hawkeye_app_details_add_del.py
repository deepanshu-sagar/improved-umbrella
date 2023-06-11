def hawkeye_app_details_add_del(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['hawkeye_app_details']
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
        canonical_id = req_data[0]
        platform = req_data[1]
        if len(req_data) == 4:
            store_id = req_data[2]
            action = req_data[3].lower()
        else:
            store_id = 0
            action = req_data[2].lower()
        if action == 'add':
            sql_texts_del.append("delete from HawkEye.app_details where canonical_id='" + canonical_id + "' and store_id=" + str(store_id) + ';')
            sql_texts_add.append("insert ignore HawkEye.app_details(canonical_id,platform_id,store_id,source) values('" + canonical_id + "'," + platform + ',' + str(store_id) + ",'automation');")
        elif action == 'remove':
            self.hawkeye_app_details_remove_new(canonical_id, platform, store_id, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(canonical_id))
    q1 = '\n'.join(sql_texts_del)
    print(q1)
    self.execute_sql_db_multi(q1, db_server, db_user, db_password, db_port, 'HawkEye')
    q2 = '\n'.join(sql_texts_add)
    print(q2)
    self.execute_sql_db_multi(q2, db_server, db_user, db_password, db_port, 'HawkEye')