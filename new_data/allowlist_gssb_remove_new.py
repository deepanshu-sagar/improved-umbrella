def gssb_remove_new(self, domain, platform, store_id, db_server, db_port, db_user, db_password):
    print('removing domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "delete from KomliAdServer.global_supply_side_blocklist where domain='" + domain + "' and store_id=" + str(store_id) + ';'
    print(sql)
    mycursor.execute(sql)
    mydb.commit()