import pika
import json


class get_rabbitmq:
    def __init__(self):
        # 获取与rabbitmq 服务的连接，虚拟队列需要指定参数 virtual_host，如果是默认的可以不填（默认为/)，也可以自己创建一个
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.201', port=5672,
                                                                            credentials=pika.PlainCredentials("admin",
                                                                                                              "jbsrmqAdmin")))
        # 创建一个 AMQP 信道（Channel）
        self.channel = self.connection.channel()

    # 定义生产者并将消息推送到指定的交换机
    def producter(self, exchange, queue, message, routing_key=None):
        # 声明消息队列 ,消息将在这个队列传递
        self.channel.queue_declare(queue, durable=True)
        # 将信息指定推送的对应的 交换机-exchange,路由key-routing_key,推送消息-message
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,properties = pika.BasicProperties(content_type="text/plain",content_encoding="UTF-8"))
        # 关闭连接
        self.channel.close()
        # 定义生产者并将消息推送到指定的交换机

    # def producter(self, exchange, message, routing_key=None):
    #     # 声明消息队列 ,消息将在这个队列传递
    #     self.channel.queue_declare(queue, durable=True)
    #     # 将信息指定推送的对应的 交换机-exchange,路由key-routing_key,推送消息-message
    #     self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    #     # 关闭连接
    #     self.channel.close()
