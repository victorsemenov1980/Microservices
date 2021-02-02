 # -*- coding: utf-8 -*-
import pika, json, os, django


os.environ.setdefault('DJANGO_SETTINGS_MODULE','admin.settings')
django.setup()
from products.models import Product

params=pika.URLParameters('amqps://kgeiibqf:tFDehiYv1Rgctu3l7J4sh8pjEExaxNbS@owl.rmq.cloudamqp.com/kgeiibqf')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch,method,properties,body):
    print('Received in admin')
    data=json.loads(body)
    '''
    Here we got to publish data to Redis
    '''
    if properties.content_type=='product list sent':
        
        print('Product list published')
    
    return data
    

channel.basic_consume(queue='admin',on_message_callback=callback,auto_ack=True)

print( 'Started Consuming')
channel.start_consuming()

channel.close()
