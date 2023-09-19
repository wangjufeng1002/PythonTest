import db




if __name__ == '__main__':
    move_stock_order_all = db.get_move_stock_order()
    move_stock_order_detail_all = db.get_move_stock_order_detail()



    move_stock_order_map = {}
    for move_stock_order in move_stock_order_all:
        move_stock_order_map[move_stock_order['move_stock_id']]=move_stock_order
