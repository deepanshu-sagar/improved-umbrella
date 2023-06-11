def gssb_add_new(self, domain, platform, store_id, db_server, db_port, db_user, db_password):
    self.gssb_remove_new(domain, platform, store_id, db_server, db_port, db_user, db_password)
    print('adding domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "insert ignore KomliAdServer.global_supply_side_blocklist(domain,platform_id,store_id,reason)values('" + domain + "'," + platform + ',' + str(store_id) + ",'automation');"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()