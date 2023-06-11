def gcpb_remove(self, domain, platform, db_server, db_port, db_user, db_password):
    print('removing domain')
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), passwd=str(db_password), port=str(db_port), database='KomliAdServer')
    mycursor = mydb.cursor()
    sql = "delete from KomliAdServer.global_channel_partner_block_list where domain='" + domain + "';"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()