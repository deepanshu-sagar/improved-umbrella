def get_publisher_site_allowlist_db_data(self, tld_names, user, db_user, db_password, db_host, port):
    """
        Fetches Data from DB
        :param tld_names:
        :return:
        """
    mydb = mysql.connector.connect(host=str(db_host), user=str(db_user), passwd=str(db_password), port=str(port), database='BulkOpsMgmt')
    rows_query = "SELECT tld_name as 'Domain Name', status as Status, store_id as 'CTV App Store', description as Description FROM BulkOpsMgmt.staging_publisher_aggregator_site_tld WHERE tld_name ='{0}' and pub_id= {1};".format(tld_names, str(user))
    print(rows_query)
    all_df = pd.read_sql(rows_query, mydb)
    status_replace_values = {0: 'Approved'}
    store_replace_values = {0: 'NA', 3: 'Roku', 999999: 'Other'}
    all_df['Status'] = all_df['Status'].map(status_replace_values)
    all_df['CTV App Store'] = all_df['CTV App Store'].map(store_replace_values)
    print(all_df)
    return all_df