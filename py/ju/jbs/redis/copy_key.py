import redis

# 线上 online_redis 是线上redis ，禁止调用写入
online_redis = redis.StrictRedis(host="r-2zeobgvphjbjrah3y4pd.redis.rds.aliyuncs.com", port='16379', username='redis',
                                 password='63AF*hNU&da!Jo')

# 线上
test_redis = redis.StrictRedis(host="omsstage.redis.rds.aliyuncs.com", port='16379', password='jOKu@$g%yGjmQZ')

test_redis.set("AAA-shuji", "高永康，书记，")

shop_advertiser_112 = online_redis.hgetall("QIANCHUAN_ADVERTISER_TOKEN_1785713382746169")

advertiser_token_112 = online_redis.hgetall("QIANCHUAN_ADVERTISER_TOKEN_1785713382746169")

test_redis.hset("QIANCHUAN_ADVERTISER_TOKEN_1785713382746169", mapping=shop_advertiser_112)
test_redis.hset("QIANCHUAN_ADVERTISER_TOKEN_1785713382746169", mapping=advertiser_token_112)
