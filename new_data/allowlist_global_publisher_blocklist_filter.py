def global_publisher_blocklist_filter(self, test_data, db_server, db_port, db_user, db_password):
    request_line = test_data['gssb_filter']
    if str(request_line).lower().strip() == 'none':
        return
    insert_sql = 'insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id)values'
    delete_sql = 'delete from KomliAdServer.global_supply_side_blocklist where '
    print('inside GPBL filter')
    if request_line == 'none':
        print('no daata to process')
        return
    req_lines = request_line.split('\n')
    for line in req_lines:
        req_data = line.split(',')
        domain = req_data[0]
        platform = req_data[1]
        action = req_data[2].lower()
        if action == 'add':
            print('adding')
            self.gssb_add(domain, platform, db_server, db_port, db_user, db_password)
        elif action == 'remove':
            self.gssb_remove(domain, platform, db_server, db_port, db_user, db_password)
        else:
            print('invalid action found for domain ' + str(domain))