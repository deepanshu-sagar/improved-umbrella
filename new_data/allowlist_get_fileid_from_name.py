def get_fileid_from_name(self, db_server, db_port, db_user, db_password):
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), port=str(db_port), passwd=str(db_password), database='ActivityLog')
    mycursor = mydb.cursor()
    sql = "select id  from bulk_operations where  file_name ='" + str(self.activity_file_name) + "'; "
    print(sql)
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if isinstance(data, tuple):
        for x in data:
            return x
        print('sleeping')
        mydb.commit()
    raise Exception('Bulk file not found')