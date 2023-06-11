def execute_sql_db_multi(self, sql, db_server, db_user, db_password, db_port, db):
    mydb = mysql.connector.connect(host=str(db_server), user=str(db_user), port=str(db_port), passwd=str(db_password), database=str(db))
    mycursor = mydb.cursor()
    select_out = []
    for result in mycursor.execute(sql, multi=True):
        if result.with_rows:
            out = result.fetchall()
            select_out.append(out)
        else:
            pass
    mydb.commit()
    return select_out