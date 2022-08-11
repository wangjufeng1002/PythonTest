import redis


redis_info = {
    "host": "192.168.1.201",
    "password": "jbsDBredis",
    "port": 7001,
    "db": 0
}

r = redis.Redis(**redis_info, decode_responses=True)
print(r.hgetall("wms_delivery_order_action_lock"))

#r.delete("wms_delivery_order_action_lock")