# -*- coding: utf-8 -*-

import pika
import json

params=pika.URLParameters('amqps://kgeiibqf:tFDehiYv1Rgctu3l7J4sh8pjEExaxNbS@owl.rmq.cloudamqp.com/kgeiibqf')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method,body):
    properties=pika.BasicProperties(method)
    channel.basic_publish(exchange='',routing_key='main', body=json.dumps(body),properties=properties)

