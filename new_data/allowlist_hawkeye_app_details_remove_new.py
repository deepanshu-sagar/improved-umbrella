def hawkeye_app_details_remove_new(self, canonical_id, platform, store_id, db_server, db_port, db_user, db_password):
    print('removing domain from hawkeye db - app details table')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='HawkEye')
    mycursor = mydb.cursor()
    sql = "delete from HawkEye.app_details where canonical_id='" + canonical_id + "'and platform_id='" + platform + "' and store_id=" + str(store_id) + ';'
    print(sql)
    mycursor.execute(sql)
    mydb.commit()