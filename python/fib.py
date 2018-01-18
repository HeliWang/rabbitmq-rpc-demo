#!/usr/bin/env python
import pika
import json
import sys

connection = pika.BlockingConnection(pika.URLParameters("amqp://rxuhxbbh:mkywerCtgEVDC-LOARLwgi7mm4xhteZA@white-swan.rmq.cloudamqp.com/rxuhxbbh"))
channel = connection.channel()

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def publish_back():
    body = json.load(sys.stdin)
    n = int(body['n'])
    print(" [.] fib(%s)" % n)
    response = fib(n)
    channel.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    channel.basic_ack(delivery_tag=method.delivery_tag)

publish_back()