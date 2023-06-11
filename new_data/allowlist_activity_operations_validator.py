def activity_operations_validator(self, db_server, db_port, db_user, db_password, file_name):
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), port=str(db_port), passwd=str(db_password), database='ActivityLog')
    flag = False
    for i in range(1, 200):
        mycursor = mydb.cursor()
        sql = "select status  from bulk_operations where  file_name ='" + str(file_name) + "'; "
        print(sql)
        mycursor.execute(sql)
        data = mycursor.fetchone()
        if isinstance(data, tuple):
            for x in data:
                print(x)
                if x == '1':
                    flag = True
        if flag == True:
            print('bulk operation validated!')
            return
        time.sleep(1)
        print('sleeping')
        mydb.commit()
    raise Exception('bulk operation failed!')