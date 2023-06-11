def get_publisher_allowlist_db_data(self, tld_names, db_user, db_password, db_host, port):
    """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
    print('running get_publisher_allowlist_db_data')
    mydb = mysql.connector.connect(host=str(db_host), user=str(db_user), passwd=str(db_password), port=str(port), database='fraud_mgmt')
    rows_query = "SELECT adserving_entity as 'Domain / App ID', platform_id as Platform, store_id as Store FROM fraud_mgmt.publisher_allowlist WHERE adserving_entity ='{}';".format(tld_names)
    print(rows_query)
    all_df = pd.read_sql(rows_query, mydb)
    platform_replace_values = {1: 'Web', 2: 'Mobile Web', 4: 'Mobile App IOS', 5: 'Mobile App Android', 7: 'CTV'}
    store_id_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
    all_df['Platform'] = all_df['Platform'].map(platform_replace_values)
    all_df['Store'] = all_df['Store'].map(store_id_replace_values)
    print(all_df)
    return all_df