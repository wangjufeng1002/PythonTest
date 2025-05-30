from toollib.guid import SnowFlake
import time
import random
import json

from py.ju.jbs.mes.order_plan import mq

material_codes = ["6000-02-BCP003", "6000-03-YCL043", "MAT-LJT", "6000-03-BCP-4J-001", "6000-01-CP007"]

master_material_codes=["JBS-TS-CK1A-JWT","MEY-JMTB-33S01-GOG2P","JBS-ZWJ-SJ201-HS"]

purchase_material_codes = ['6000-03-BCP-4J-001',
'6000-03-YCL001',
'6000-03-BCP-5J-001',
'MAT-LJT',
'6000-03-YCL042',
'6000-03-YCL041',
'6000-01-CP007',
'6000-03-YCL043']

def get_purchase_order_id():
    # snowflake.client.setup("localhost", 8910)
    # guid = snowflake.client.get_guid()
    snow = SnowFlake()
    guid = snow.gen_uid()
    return "PO" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)
def get_id():
    # snowflake.client.setup("localhost", 8910)
    # guid = snowflake.client.get_guid()
    snow = SnowFlake()
    return  snow.gen_uid()

def get_purchase_line_id():
    # snowflake.client.setup("localhost", 8910)
    # guid = snowflake.client.get_guid()
    snow = SnowFlake()
    guid = snow.gen_uid()
    return "PLINE" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)

def get_plan_order():
    snow = SnowFlake()
    guid = snow.gen_uid()
    return "PLINE" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(random.randint(1, 1000000)) + str(guid)

def send_create_msg():
    order_id = get_purchase_order_id()
    lines = []
    for i in range(0, random.randint(1, 5)):
        line = {}
        line["demandNum"] = random.randint(50, 1000)
        line["freightPrice"] = 10
        line["goodsCode"] = random.choice(master_material_codes)
        line["purchaseOrderId"] = order_id
        line["receiveWarehouseCode"] = "WH0001"
        line["requireDeliveryDate"] = 1721956049000
        line["supplierCode"] = "G100109"
        line["purchaseLineId"] = get_purchase_line_id()
        lines.append(line)

    msg_map = {"purchaseOrderId": order_id, "modifyPurchaseLines": lines}
    mq.get_rabbitmq().producter(exchange='srm-ops_purchase.order_modify_mes-order',
                                queue='srm-ops_purchase.order_modify_mes-order',
                                routing_key='srm-ops_purchase.order_modify_mes-order',
                                message=json.dumps(msg_map, ensure_ascii=False))



def send_purchase_inbound_create_msg():
    msgId = get_id()
    items = []
    for i in range(0, random.randint(1, 5)):
        item = {}
        item["stockOrderId"] = get_id()
        item["sourceOrderId"] = 10
        item["warehouseCode"] = 'WH0476'
        item["ownerCode"] = "OW003"
        item["evaluateArrivedDate"] = 1719833553000
        item["inTransitNum"] = random.randint(1, 1000)
        item["materialCode"] = random.choice(purchase_material_codes)
        items.append(item)

    msg_map = {"msgId": msgId, "purchaseItems": items}
    mq.get_rabbitmq().producter(exchange='imc_purchase_inbound_create_mes-order',
                                queue='imc_purchase_inbound_create_mes-order',
                                routing_key='imc_purchase_inbound_create_mes-order',
                                message=json.dumps(msg_map, ensure_ascii=False))


if __name__ == '__main__':
    #send_create_msg()
    send_purchase_inbound_create_msg()
