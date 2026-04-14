# kafka-producer-consumer
a simple kafka env with producer and consumer

### run
`docker compose up --build` \
terminal1: `uv run consumer.py` \
terminal2: `uv run producer.py`

### kafka CLI
https://docs.confluent.io/kafka/operations-tool/kafka-tools.html#ak-command-line-interface-cli-tools

`docker compose exec kafka bash` \
`/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092` \
`/opt/kafka/bin/kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092` \
`/opt/kafka/bin/kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092` \
`/opt/kafka/bin/kafka-topics.sh --describe --topic test-topic --bootstrap-server localhost:9092` \
`/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders  --from-beginning`

### 3 alternatives to topic creation
* enter container bash and run topic creation command
* leave creation to producer the moment first message is sent
* run an init container that creates the topic and shuts down

### Listeners config
Naming KAFKA_LISTENERS with PLAINTEXT is a standard Kafka convention for defining unencrypted TCP listeners. \
PLAINTEXT serves as both a built-in name and protocol identifier for simplicity, plus is predefined and avoids extra mapping. \
INTERNAL and EXTERNAL are used in this case as `kafka-init` client is within Docker whereas `producer.py` and `consumer.py` are outside Docker (running in local machine) so accessing Kafka from different routes (see https://docs.docker.com/guides/kafka/#defining-the-listeners)
<img width="1091" height="660" alt="image" src="https://github.com/user-attachments/assets/5eba0633-ba6d-435c-b0d3-60a0cab85bbc" />

### Warning
`error WARN [AdminClient clientId=adminclient-1] Connection to node 1 could not be established. Node may not be available.` \
This is due to the `command:` running before the broker is up and running. \
Since `command:` OVERWRITE the default command `kafka-server-start.sh`, the broker has to be up and running the moment the command is applyed:
* use `service_healthy` to wait the broker is up before running the topic creation
* properly configure INTERNAL and EXTERNAL to Docker clients for correct networking
