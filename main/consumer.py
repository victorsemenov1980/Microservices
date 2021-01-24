# -*- coding: utf-8 -*-
import pika,json
from main import Product, db

params=pika.URLParameters('amqps://kgeiibqf:tFDehiYv1Rgctu3l7J4sh8pjEExaxNbS@owl.rmq.cloudamqp.com/kgeiibqf')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch,method,properties,body):
    print('Received in admin')
    data=json.loads(body)
    print(data)
    
    if properties.content_type=='product created':
        product=Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')
    
    elif properties.content_type=='product updated':
        product=Product.query.get(data['id'])
        product.title=data['title']
        product.image=data['image']
        db.session.commit()
        print('Product changed')
    
    elif properties.content_type=='product deleted':
        product=Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')

channel.basic_consume(queue='main',on_message_callback=callback, auto_ack=True)

print( 'Started Consuming')
channel.start_consuming()

channel.close()

































