import json
from confluent_kafka import Consumer

consumer = Consumer({
    'bootstrap.servers':'localhost:9093', # endpoint for clients outside docker
    'group.id': 'order-group', # replicate consumers (n instances) and group them to scale in case of load spike
    'auto.offset.reset': 'earliest' # when consumer connects start reading from beginning
})

consumer.subscribe(['orders'])

print('🔵 consumer running...')

try:
    # check continuously if there are new events in the topic
    while True:
        msg = consumer.poll(1.0) # consumers poll new msg, not kafka sending them
        if msg is None:
            continue
        if msg.error():
            print(f'🔴 Error: {msg.error()}')
            continue

        value = msg.value().decode('utf-8')
        order = json.loads(value) # string to dict
        print(f'🎁 Received order: {order['quantity']}, {order['item']}, from {order['user']}')

except KeyboardInterrupt:
    print('🔴 stopping consumer ...')

finally:
    consumer.close()

# close() is crucial for properly release resources associated with consumer instance
# ensures that network connections and file handles are closed, offsets committed and consumer's partition assignments revoked