#!/usr/bin/env python
import pika
import json
import sys
from urllib.parse import unquote

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def publish_back():
    connection = pika.BlockingConnection(pika.URLParameters("amqp://rxuhxbbh:mkywerCtgEVDC-LOARLwgi7mm4xhteZA@white-swan.rmq.cloudamqp.com/rxuhxbbh"))
    ch = connection.channel()
    ch.queue_declare(queue='rpc_queue')
    body = json.loads(unquote(sys.argv[1]))
    print(body)
    n = int(body['n'])
    reply_to = body['reply_to']
    correlation_id = body['correlation_id']
    response = fib(n)
    ch.basic_publish(exchange='',
                     routing_key=reply_to,
                     properties=pika.BasicProperties(correlation_id=correlation_id),
                     body=str(response))
    print(" [x] Sent " + str(response) + " to " + reply_to)
    connection.close()

publish_back()