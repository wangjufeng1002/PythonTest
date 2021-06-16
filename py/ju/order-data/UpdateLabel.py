import db

if __name__ == '__main__':
    db.initDb("test")
    ids = db.getOrderIds(24021)
    for id in ids:
        label = db.getOrderLabel(id)
        if label is not None and len(label) > 1 :
            db.updateOrdersLabel(orderId=id, label=str(label.get("orderLable")), labelDesc=label.get("orderLableComment"))
            print(id)







