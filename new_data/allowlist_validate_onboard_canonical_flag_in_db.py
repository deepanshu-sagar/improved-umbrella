def validate_onboard_canonical_flag_in_db(self, pub_id, flag, fraud_db_host, user_name, password, port):
    mydb = mysql.connector.connect(host=str(fraud_db_host), user=str(user_name), port=str(port), passwd=str(password), database=str('fraud_mgmt'))
    query = f'select onboarding_canonical from publisher_iq_settings where pub_id={pub_id} and onboarding_canonical={flag}'
    mycursor = mydb.cursor()
    print(query)
    mycursor.execute(query)
    result = mycursor.fetchone()
    print(result)
    if result is None:
        assert flag != flag