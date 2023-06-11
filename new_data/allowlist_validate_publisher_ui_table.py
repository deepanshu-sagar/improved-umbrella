def validate_publisher_ui_table(self, test_data, db_user_name, db_password, db_host, db_port, activity_logs_db_user_name, activity_logs_db_password, activity_logs_db_host, activity_logs_db_port, uri_prefix, token, user):
    self.find_domain_publisher_allowlist(test_data.split(',')[0])
    print('find completed')
    df_db = self.get_publisher_allowlist_db_data(test_data.split(',')[0], db_user_name, db_password, db_host, int(db_port))
    print('dataframe database')
    print(df_db)
    print(test_data.split(',')[1])
    if test_data.split(',')[1] != 'CTV':
        print(test_data.split(',')[1])
        crc_64 = self.calculate_crc64(test_data.split(',')[0])
        print(str(crc_64))
    else:
        if test_data.split(',')[2] == 'Roku':
            store = '3'
        else:
            store = '999999'
        crc = '{0}_{1}'.format(store, test_data.split(',')[0])
        crc_64 = self.calculate_crc64(crc)
        print(crc_64)
    df_db.rename(columns={'domain': 'Domain / App ID', 'platform_id': 'Platform', 'store_id': 'Store'}, inplace=True)
    df_ui = self.acc7.pmccTable('dt-table')
    df_ui = df_ui.drop([''], axis=1)
    df_ui = df_ui.drop('Status', axis=1)
    df_ui = df_ui.drop('Error Description', axis=1)
    print('DB DATAFRAME')
    print(df_db)
    print('UI DATAFRAME')
    print(df_ui)
    self.search_in_df(df_ui, df_db)
    self.validate_download_all_pub_allow(test_data.split(',')[0], uri_prefix, token, user)