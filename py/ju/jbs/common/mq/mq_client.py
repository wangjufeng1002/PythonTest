import pika
import json
from ju.jbs.common.config.mq_config import (
    dev_host, dev_port, dev_virtual_host, dev_username, dev_password,
    online_host, online_port, online_virtual_host, online_username, online_password
)


class MQClient:
    def __init__(self, online: bool = False):
        # 获取与rabbitmq 服务的连接
        if online is False:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=dev_host, port=dev_port, virtual_host=dev_virtual_host,
                                          credentials=pika.PlainCredentials(dev_username,
                                                                            dev_password)))
        else:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=online_host, port=online_port, virtual_host=online_virtual_host,
                                          credentials=pika.PlainCredentials(online_username, online_password)))
        # 创建一个 AMQP 信道（Channel）
        self.channel = self.connection.channel()

    # 定义生产者并将消息推送到指定的交换机
    def send_message(self, exchange, message, routing_key=None, queue=None):
        # 声明消息队列 ,消息将在这个队列传递
        if queue is not None:
            self.channel.queue_declare(queue, durable=True)
        # 将信息指定推送的对应的 交换机-exchange,路由key-routing_key,推送消息-message
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,
                                   properties=pika.BasicProperties(content_type="text/plain", content_encoding="UTF-8"))

    # 定义生产者并将消息推送到指定的交换机（带队列声明）
    def send_message_with_queue(self, exchange, queue, message, routing_key=None):
        # 声明消息队列 ,消息将在这个队列传递
        self.channel.queue_declare(queue, durable=True)
        # 将信息指定推送的对应的 交换机-exchange,路由key-routing_key,推送消息-message
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,
                                   properties=pika.BasicProperties(content_type="text/plain", content_encoding="UTF-8"))
        # 关闭连接
        self.channel.close()

    def close(self):
        self.channel.close()
