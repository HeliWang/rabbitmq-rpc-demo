#!/usr/bin/env python
import pika
import json
from subprocess import Popen
import sys
from urllib.parse import quote

DETACHED_PROCESS = 0x00000008


connection = pika.BlockingConnection(pika.URLParameters("amqp://rxuhxbbh:mkywerCtgEVDC-LOARLwgi7mm4xhteZA@white-swan.rmq.cloudamqp.com/rxuhxbbh"))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):
    body = json.loads(body)
    model = body['model']
    print(" Processing " + model)
    body['reply_to'] = props.reply_to
    body['correlation_id'] = props.correlation_id
    cmd = [
        'python',
         model + '.py',
         quote(json.dumps(body))
    ]
    print(json.dumps(body))
    p = Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True, creationflags=DETACHED_PROCESS)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting Model Inference RPC requests")
channel.start_consuming()