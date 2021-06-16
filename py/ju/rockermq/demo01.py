#!/usr/bin/python
# -*- coding: UTF-8 -*-
from rocketmq.client import PullConsumer
consumer = PullConsumer('CID_XXX')
consumer.set_namesrv_addr('192.168.0.1:9876')
consumer.start()
