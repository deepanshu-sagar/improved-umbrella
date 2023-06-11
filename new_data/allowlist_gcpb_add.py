def gcpb_add(self, domain, platform, db_server, db_port, db_user, db_password):
    self.gcpb_remove(domain, platform, db_server, db_port, db_user, db_password)
    print('adding domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "insert ignore KomliAdServer.global_channel_partner_block_list(domain,platform_id)values('" + domain + "'," + platform + ');'
    print(sql)
    mycursor.execute(sql)
    mydb.commit()