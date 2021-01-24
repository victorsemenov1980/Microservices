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
    id=json.loads(body)
    print(id)
    product=Product.objects.get(id=id)
    product.choices=product.choices+1
    product.save()
    print('Product chosen count increased')

channel.basic_consume(queue='admin',on_message_callback=callback,auto_ack=True)

print( 'Started Consuming')
channel.start_consuming()

channel.close()
