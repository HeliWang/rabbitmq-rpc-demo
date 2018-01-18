#!/usr/bin/env python
import pika
import json
from threading import Timer

connection = pika.BlockingConnection(pika.URLParameters("amqp://rxuhxbbh:mkywerCtgEVDC-LOARLwgi7mm4xhteZA@white-swan.rmq.cloudamqp.com/rxuhxbbh"))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    body = json.loads(body)
    n = int(body['n'])

    print(" [.] fib(%s)" % n)

    response = fib(n)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # response = {fib_result: fib(n)}
    # json.dumps(response))

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting Model Inference RPC requests")
channel.start_consuming()