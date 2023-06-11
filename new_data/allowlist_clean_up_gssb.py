def clean_up_gssb(self, test_data, Komli_db_server, db_port, db_user, db_password):
    print('insite clean_up_gssb...!')
    publisher_allowlist_records = test_data['publisher_allowlist_records']
    if str(publisher_allowlist_records).lower().strip() == 'none':
        return
    records = publisher_allowlist_records.split('\n')
    sql_texts = []
    for record in records:
        data = record.split(',')
        adserving_entity = data[0]
        platform_id = data[1]
        if platform_id in ['1', '2']:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
        else:
            sql_texts.append("delete from KomliAdServer.global_supply_side_blocklist where domain='" + str(adserving_entity) + "';")
    q = '\n'.join(sql_texts)
    print(q)
    self.execute_sql_db_multi(q, Komli_db_server, db_user, db_password, db_port, 'KomliAdServer')