
import json
from pymysql_comm import UsingOnlineOMS as online
msgStr = "{\"deliveryOrderDetails\":[{\"actualReceiveNum\":884,\"arriveNum\":884,\"goodsCode\":\"JBS-BLCB-N03-1P\",\"purchaseLineId\":\"1925464289297399808\",\"rejectNum\":0},{\"actualReceiveNum\":116,\"arriveNum\":116,\"goodsCode\":\"JBS-BLCB-N03-1P\",\"purchaseLineId\":\"1923216268064915457\",\"rejectNum\":0},{\"actualReceiveNum\":600,\"arriveNum\":600,\"goodsCode\":\"JBS-BLCB-N04-01\",\"purchaseLineId\":\"1923213767727054848\",\"rejectNum\":0},{\"actualReceiveNum\":400,\"arriveNum\":400,\"goodsCode\":\"JBS-BLCB-N04-01\",\"purchaseLineId\":\"1925465881941565442\",\"rejectNum\":0},{\"actualReceiveNum\":745,\"arriveNum\":745,\"goodsCode\":\"JBS-BLCB-N15-01\",\"purchaseLineId\":\"1922540655633096709\",\"rejectNum\":0},{\"actualReceiveNum\":200,\"arriveNum\":200,\"goodsCode\":\"JBS-BLCB-N15-01\",\"purchaseLineId\":\"1920661888258215936\",\"rejectNum\":0},{\"actualReceiveNum\":55,\"arriveNum\":55,\"goodsCode\":\"JBS-BLCB-N15-01\",\"purchaseLineId\":\"1922540655633096711\",\"rejectNum\":0},{\"actualReceiveNum\":557,\"arriveNum\":557,\"goodsCode\":\"JBS-BLCB-S05C-02\",\"purchaseLineId\":\"1874660649427226636\",\"rejectNum\":0},{\"actualReceiveNum\":443,\"arriveNum\":443,\"goodsCode\":\"JBS-BLCB-S05C-02\",\"purchaseLineId\":\"1874660649427226638\",\"rejectNum\":0},{\"actualReceiveNum\":77,\"arriveNum\":77,\"goodsCode\":\"JBS-JMTB-M031S-33GOG2P\",\"purchaseLineId\":\"1918575446212153344\",\"rejectNum\":0},{\"actualReceiveNum\":1400,\"arriveNum\":1400,\"goodsCode\":\"JBS-MT-38T1-01\",\"purchaseLineId\":\"1918571830101471232\",\"rejectNum\":0},{\"actualReceiveNum\":900,\"arriveNum\":900,\"goodsCode\":\"JBS-MT-N38-GY\",\"purchaseLineId\":\"1922540655641485316\",\"rejectNum\":0},{\"actualReceiveNum\":100,\"arriveNum\":100,\"goodsCode\":\"JBS-MT-N38-GY\",\"purchaseLineId\":\"1922540655641485314\",\"rejectNum\":0},{\"actualReceiveNum\":897,\"arriveNum\":897,\"goodsCode\":\"JBS-MT-N701-33GY\",\"purchaseLineId\":\"1922540655649873925\",\"rejectNum\":0},{\"actualReceiveNum\":103,\"arriveNum\":103,\"goodsCode\":\"JBS-MT-N701-33GY\",\"purchaseLineId\":\"1925460067516243968\",\"rejectNum\":0},{\"actualReceiveNum\":2258,\"arriveNum\":2258,\"goodsCode\":\"JBS-MT-T1-2803\",\"purchaseLineId\":\"1920661955471937536\",\"rejectNum\":0},{\"actualReceiveNum\":442,\"arriveNum\":442,\"goodsCode\":\"JBS-MT-T1-2803\",\"purchaseLineId\":\"1922540655624708096\",\"rejectNum\":0},{\"actualReceiveNum\":300,\"arriveNum\":300,\"goodsCode\":\"JBS-MT-T1-2803\",\"purchaseLineId\":\"1922540655624708098\",\"rejectNum\":0},{\"actualReceiveNum\":2000,\"arriveNum\":2000,\"goodsCode\":\"JBS-MT-T1-3301\",\"purchaseLineId\":\"1918591468633710592\",\"rejectNum\":0},{\"actualReceiveNum\":542,\"arriveNum\":542,\"goodsCode\":\"JBS-PB-G1D1-01\",\"purchaseLineId\":\"1918574221483696128\",\"rejectNum\":0},{\"actualReceiveNum\":268,\"arriveNum\":268,\"goodsCode\":\"JBS-PB-G1D1-01\",\"purchaseLineId\":\"1923306491365130240\",\"rejectNum\":0},{\"actualReceiveNum\":100,\"arriveNum\":100,\"goodsCode\":\"JBS-PB-G1D1-01\",\"purchaseLineId\":\"1925463232622026752\",\"rejectNum\":0},{\"actualReceiveNum\":90,\"arriveNum\":90,\"goodsCode\":\"JBS-PB-G1D1-01\",\"purchaseLineId\":\"1928353171617705984\",\"rejectNum\":0},{\"actualReceiveNum\":2790,\"arriveNum\":2790,\"goodsCode\":\"JBS-QJT-S03-CH\",\"purchaseLineId\":\"1925444587128709120\",\"rejectNum\":0},{\"actualReceiveNum\":2995,\"arriveNum\":2995,\"goodsCode\":\"JBS-SCS-N02-JWT\",\"purchaseLineId\":\"1920665166882738176\",\"rejectNum\":0},{\"actualReceiveNum\":1505,\"arriveNum\":1505,\"goodsCode\":\"JBS-SCS-N02-JWT\",\"purchaseLineId\":\"1925459580234858496\",\"rejectNum\":0},{\"actualReceiveNum\":978,\"arriveNum\":978,\"goodsCode\":\"JBS-TBB-N0133-01\",\"purchaseLineId\":\"1924634846710562816\",\"rejectNum\":0},{\"actualReceiveNum\":711,\"arriveNum\":711,\"goodsCode\":\"JBS-TBB-N0133-01\",\"purchaseLineId\":\"1925462386555412481\",\"rejectNum\":0},{\"actualReceiveNum\":311,\"arriveNum\":311,\"goodsCode\":\"JBS-TBB-N0133-01\",\"purchaseLineId\":\"1923219091716505600\",\"rejectNum\":0},{\"actualReceiveNum\":1710,\"arriveNum\":1710,\"goodsCode\":\"JBS-TBB-S0233-01\",\"purchaseLineId\":\"1925459981172301824\",\"rejectNum\":0},{\"actualReceiveNum\":1011,\"arriveNum\":1011,\"goodsCode\":\"JBS-TBB-S0233-01\",\"purchaseLineId\":\"1923215257111908352\",\"rejectNum\":0},{\"actualReceiveNum\":139,\"arriveNum\":139,\"goodsCode\":\"JBS-TBB-S0233-01\",\"purchaseLineId\":\"1925460128597991424\",\"rejectNum\":0},{\"actualReceiveNum\":124,\"arriveNum\":124,\"goodsCode\":\"JBS-TBB-S0233-01\",\"purchaseLineId\":\"1902626854045499392\",\"rejectNum\":0},{\"actualReceiveNum\":16,\"arriveNum\":16,\"goodsCode\":\"JBS-TBB-S0233-01\",\"purchaseLineId\":\"1921719341003509760\",\"rejectNum\":0}],\"mesDeliveryOrderId\":\"MFH2505301928319557136965632\",\"msgId\":\"1928993903458141256\",\"receiveTime\":1748585612000}";


def get_delivery_order_detail(delivery_order_id):

    sql = "SELECT * FROM `mes_order`.`delivery_order_detail` where delivery_order_id = '{order_id}' ".format(order_id =delivery_order_id)
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()
def get_sales_order(sales_order_ids):
    ids = ','.join(repr(str(id)) for id in sales_order_ids)
    sql = "SELECT * FROM `mes_order`.`sales_order` where sales_order_id in (%s) " % ids
    with online() as um:
        um.cursor.execute(sql)
        return um.cursor.fetchall()
if __name__ == '__main__':


    sql_template = ("update mes_order.sales_order set in_transit_num = in_transit_num + {num} , receive_num = receive_num-{num} ,actual_receive_num=  actual_receive_num-{num} "
                    "where  sales_order_id = '{salesOrderId}' and  purchase_line_id = '{purchaseLineId}' ;")
    msg = json.loads(msgStr)
    details_ = msg['deliveryOrderDetails']

    purchase_sales_map = {}
    delivery_order_details = get_delivery_order_detail(msg['mesDeliveryOrderId'])
    sales_order_id = []
    for delivery_order_detail in delivery_order_details:
        sales_order_id.append(delivery_order_detail['sales_order_id'])

    orders = get_sales_order(sales_order_id)
    for order in orders:
        purchase_sales_map[order['purchase_line_id']] = order['sales_order_id']

    for detail in details_:
        print(detail['purchaseLineId'])
        # print(detail['actualReceiveNum'])
        print(sql_template.format(num=detail['actualReceiveNum'],
                                  salesOrderId=purchase_sales_map[detail['purchaseLineId']],
                                  purchaseLineId=detail['purchaseLineId']))
