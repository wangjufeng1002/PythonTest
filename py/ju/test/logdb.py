import pymysql

conn = pymysql.connect(host="10.255.254.225", port=3307, user="writeuser", password="ddbackend", database="openapi_logs",
                       charset="utf8")

sql = "insert into AAA(method,app_key,v,session,agent_type) values "
value = "('%s','%s','%s','%s','%s') "

def insert(logs):
    cursor = conn.cursor()
    v =sql
    for log in logs:
        v = v + value%(log[0],log[1],log[2],log[3],log[4]) + ","
    if v is None or len(v) == 0:
        return
    exSql = v[:len(v)-1]
    cursor.execute(exSql)
    conn.commit()
    cursor.close()
    #print(exSql)


