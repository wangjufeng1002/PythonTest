import json
import mq
from py.ju.jbs.utils.pymysql_comm import UsingDev as oms_dev
from py.ju.jbs.utils.pymysql_comm import UsingOnlineOMS as oms_online
from toollib.guid import SnowFlake


def get_mould_code(page_num, page_size, online):
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
        mould_res = get_mould_code(page_num, page_size, online)
        if len(mould_res) == 0:
            break
        for mould in mould_res:
            mould_codes.append(mould['mould_code'])
        page_num += 1
    return mould_codes


def send_mould_change_msg(online):
    snow = SnowFlake()
    codes = get_all_mould_code(online)
    rabbitmq = mq.get_rabbitmq(online)
    for code in codes:
        msg = {}
        msg['mouldCode'] = code
        msg['msgId'] = snow.gen_uid()
        rabbitmq.sender(exchange='mes-pms_mould_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        print("已发送" + msg["mouldCode"])
    rabbitmq.close()


def get_equipment_code(page_num, page_size, online):
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
        equipment_res = get_equipment_code(page_num, page_size, online)
        if len(equipment_res) == 0:
            break
        for equipment in equipment_res:
            equipment_codes.append(equipment['equipment_code'])
        page_num += 1
    return equipment_codes


def send_equipment_change_msg(online):
    snow = SnowFlake()
    codes = get_all_equipment_code(online)
    rabbitmq = mq.get_rabbitmq(online)
    for code in codes:
        msg = {}
        msg['equipmentCode'] = code
        msg['msgId'] = snow.gen_uid()
        # mq_http.send_post_request()
        rabbitmq.sender(exchange='mes-pms_equipment_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        print("已发送 " + msg["equipmentCode"])
    rabbitmq.close()

def send_equipment_change_msg_with_codes(online,codes):
    snow = SnowFlake()
    rabbitmq = mq.get_rabbitmq(online)
    for code in codes:
        msg = {}
        msg['equipmentCode'] = code
        msg['msgId'] = snow.gen_uid()
        # mq_http.send_post_request()
        rabbitmq.sender(exchange='mes-pms_equipment_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        print("已发送 " + msg["equipmentCode"])
    rabbitmq.close()

def send_mould_change_msg_with_codes(online, mould_codes):
    snow = SnowFlake()
    rabbitmq = mq.get_rabbitmq(online)
    for code in mould_codes:
        msg = {}
        msg['mouldCode'] = code
        msg['msgId'] = snow.gen_uid()
        rabbitmq.sender(exchange='mes-pms_mould_modify_notify_exchange', routing_key='',
                        message=json.dumps(msg, ensure_ascii=False))
        print("已发送" + msg["mouldCode"])
    rabbitmq.close()


if __name__ == '__main__':
    send_mould_change_msg(False)
    #send_equipment_change_msg(False)

    # mould_codes = ['QS2404006',
    #                'T20-S-06-2',
    #                'T20-S-06-2',
    #                'T20-S-06-2',
    #                'T20-S-06-2',
    #                'S43-S-04',
    #                'T20-S-06-2',
    #                'S43-S-04',
    #                'T20-S-06-2',
    #                'H10-S-09',
    #                'H10-S-13',
    #                'H10-S-09',
    #                'H10-S-13',
    #                'T42-S-04',
    #                'T42-S-03'
    #                ]
    #
    # send_mould_change_msg(True, mould_codes)

    # codes = [
    #     'JBS-4-ZS-13',
    #     'JBS-4-ZS-18',
    #     'JBS-4-ZS-19',
    #     'JBS-4-ZS-20',
    #     'JBS-4-ZS-21',
    #     'JBS-4-ZS-22',
    #     'JBS-4-ZS-22',
    #     'JBS-4-ZS-23',
    #     'JBS-4-ZS-23',
    #     'JBS-4-ZS-29',
    #     'JBS-4-ZS-29',
    #     'JBS-4-ZS-30',
    #     'JBS-4-ZS-30',
    #     'JBS-4-ZS-34',
    #     'JBS-4-ZS-35'
    # ]
    #send_equipment_change_msg(True, codes)
