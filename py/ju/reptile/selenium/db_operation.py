from db_connect_pool import DEV_POOL


def get_record(key: str):
    sql = "SELECT * FROM `selenium`.`video_record` where `key`= '{}' ".format(key)
    with DEV_POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def add_record(key,url,file_name):
    print("insert ")
    sql = "INSERT INTO `selenium`.`video_record` (`key`, `url`, `file_name`) VALUES ('{}', '{}', '{}');"\
        .format(key,url,file_name)
    with DEV_POOL.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.cursor().close()
        conn.commit()
