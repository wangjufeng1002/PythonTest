import json
import mq
from pymysql_comm import UsingDev as oms_dev
from pymysql_comm import UsingOnlineOMS as oms_online
from toollib.guid import SnowFlake


def get_mould_code(page_num, page_size,online):
    page_from = (page_num - 1) * page_size
    sql = "SELECT mould_code FROM mes_pms.`mould` limit %d,%d" % (
        page_from, page_size)
    with oms_online() if online else oms_dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_all_mould_code(online):
    page_num = 1
    page_size = 100
    mould_codes = []
    while True:
        mould_res = get_mould_code(page_num, page_size,online)
        if len(mould_res) == 0:
            break
        for mould in mould_res:
            mould_codes.append(mould['mould_code'])
        page_num += 1
    return mould_codes


def send_mould_change_msg(online):
    snow = SnowFlake()
    codes = get_all_mould_code(online)
    rabbitmq = mq.get_rabbitmq()
    for code in codes:
        msg = {}
        msg['mouldCode'] = code
        msg['msgId'] = snow.gen_uid()
        rabbitmq.sender(exchange='mes-pms_mould_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        print("已发送" + msg["mouldCode"])
    rabbitmq.close()


def get_equipment_code(page_num, page_size,online):
    page_from = (page_num - 1) * page_size
    sql = "SELECT equipment_code FROM mes_pms.`equipment` limit %d,%d" % (
        page_from, page_size)
    with oms_online() if online else oms_dev() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()


def get_all_equipment_code(online):
    page_num = 1
    page_size = 100
    equipment_codes = []
    while True:
        equipment_res = get_equipment_code(page_num, page_size,online)
        if len(equipment_res) == 0:
            break
        for equipment in equipment_res:
            equipment_codes.append(equipment['equipment_code'])
        page_num += 1
    return equipment_codes


def send_equipment_change_msg(online):
    snow = SnowFlake()
    codes = get_all_equipment_code(online)
    rabbitmq = mq.get_rabbitmq()
    for code in codes:
        msg = {}
        msg['equipmentCode'] = code
        msg['msgId'] = snow.gen_uid()
        rabbitmq.sender(exchange='mes-pms_equipment_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        print("已发送 " + msg["equipmentCode"])
    rabbitmq.close()


if __name__ == '__main__':
    #send_mould_change_msg(True)
    send_equipment_change_msg(True)
