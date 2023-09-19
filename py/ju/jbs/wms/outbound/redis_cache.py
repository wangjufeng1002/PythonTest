import redis
import json

# redis_info = {
#     "host": "192.168.1.201",
#     "password": "jbsDBredis",
#     "port": 7001,
#     "db": 0
# }
# r = redis.Redis(**redis_info, decode_responses=True)
# print(r.hgetall("wms_delivery_order_action_lock"))
# keys = r.hgetall("wms_delivery_order_action_lock").keys()
# print(len(keys))
#r.delete("wms_delivery_order_action_lock")


redis_info = {
    "host": "192.168.159.105",
    "port": 6379
}

r = redis.Redis(**redis_info, decode_responses=True)
print(r.get("test"))

