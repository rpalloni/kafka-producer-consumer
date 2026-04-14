import json
import uuid
import random 
from confluent_kafka import Producer

# create a new producer client with port where kafka is accessible KAFKA_ADVERTISED_LISTENERS
# bootstrap.servers: entry point for the Kafka client to connect and to discover the full set of alive brokers in the cluster
producer = Producer({'bootstrap.servers':'localhost:9093'}) # endpoint for clients outside docker

order = {
    'order_id': str(uuid.uuid4()),
    'user': random.choice(['paul', 'marc', 'sophie', 'alex', 'carl']),
    'item': random.choice(['pizza', 'yogurt', 'salad', 'coffee']),
    'quantity': random.choice([1,2,3,4,5,6,7,8])
}

# convert the dict object to kafka compatible format bytes
value = (
    json
    .dumps(order) # conver to json string
    .encode('utf-8') # convert to bytes
)

def delivery_report(err, msg):
    if err:
        print(f'🔴 Delivery failed: {err}')
    else:
        #print(dir(msg)) # msg deep inspection
        print(f'🔵 Delivered {msg.value().decode('utf-8')}') # bytes to string 
        print(f'📝 topic: {msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()}, key: {msg.key().decode('utf-8')}')
        

# add to topic 'order' (create the topic if missing)
producer.produce(
    topic='orders' # create the topic if not available
    , key='orderskey' # which partition the message is routed. ensures all msg with same key go to the same partition preserving their order within that partition. If no key is provided, Kafka distributes messages across partitions in a round-robin manner
    , partition=0 # topic will have a single partition by default
    , value=value
    , callback=delivery_report # callback tracking successful delivery
) 

# ensure buffering messages in transit to kafka are sent
producer.flush()