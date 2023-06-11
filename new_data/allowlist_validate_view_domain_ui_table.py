def validate_view_domain_ui_table(self, test_data, db_user_name, db_password, db_host, db_port, uri_prefix, token, user):
    print('validate_view_domain_ui_table')
    self.wait_for_spinner_to_disappear(100)
    site_search = "//input[@id='search']"
    self.s2l.input_text(site_search, test_data.split(',')[0])
    self.s2l.press_key(site_search, u'\\13')
    self.wait_for_spinner_to_disappear(100)
    time.sleep(5)
    view_domain_action = "(//pmcc-icon[@data-pm-id='table-action-btn'])[2]"
    self.s2l.click_element(view_domain_action)
    view_domains = "//li[.='View Domains']"
    self.s2l.click_element(view_domains)
    self.wait_for_spinner_to_disappear(100)
    self.find_domain_publisher_site_allowlist(test_data.split(',')[1])
    print('view domain search completed')
    df_db = self.get_publisher_site_allowlist_db_data(test_data.split(',')[1], user, db_user_name, db_password, db_host, int(db_port))
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
    df_ui = self.acc7.pmccTable('dt-table')
    df_ui = df_ui.drop([''], axis=1)
    print('DB DATAFRAME')
    print(df_db)
    print('UI DATAFRAME')
    print(df_ui)
    self.search_in_df(df_ui, df_db)
    filtered_allowlist = "//button[text()=' Filtered Allowlist ']"
    filtered_allowlist_df = self.download_file_and_get_DF(filtered_allowlist)
    print('filtered_allowlist df')
    print(filtered_allowlist_df)
    filtered_allowlist_df = filtered_allowlist_df.drop(['Site Identifier'], axis=1)
    filtered_allowlist_df = filtered_allowlist_df.drop(['Platform (Web/Mobile Web/Mobile App iOS/Mobile App Android/CTV)'], axis=1)
    filtered_allowlist_df['Description'] = filtered_allowlist_df['Description'].replace(np.nan, '')
    filtered_allowlist_df['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'] = filtered_allowlist_df['CTV App Store (Applicable to only CTV platform. Supported Values are Roku/Other. For others leave this field blank)'].replace(np.nan, 0)
    filtered_allowlist_df = filtered_allowlist_df.rename(columns={'Domain/App Store URL/CTV App ID/App ID/Bundle ID': 'Domain Name'})
    print('modified filtered_allowlist df')
    print(filtered_allowlist_df)
    self.search_in_df(filtered_allowlist_df, df_db)
    self.s2l.reload_page()
    go_back = "//button[text()=' Go Back ']"
    self.s2l.click_element(go_back)
    time.sleep(5)
    self.wait_for_spinner_to_disappear(100)