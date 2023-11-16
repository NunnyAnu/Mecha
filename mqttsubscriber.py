from paho.mqtt import client as mqtt_client

class MqttSubscriber:
    def __init__(self, broker, port, initial_topic):
        self.broker = broker
        self.port = port
        self.client = self.connect_mqtt()
        self.topics = [initial_topic]
        self.subscribe()

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def on_message(self, client, userdata, msg):
        if msg.topic == "python/mqtt":
            print('a:', msg.payload.decode())
        elif msg.topic == "new_topic_to_subscribe":
            print('b:', msg.payload.decode())
        elif msg.topic == "/mqtt/testnun":
            print('b:', msg.payload.decode())
        return msg.payload.decode()

    def subscribe(self):
        self.client.on_message = self.on_message
        for topic in self.topics:
            self.client.subscribe(topic)

    def add_subscription(self, new_topic):
        self.topics.append(new_topic)
        self.client.subscribe(new_topic)

    def run(self):
        self.client.loop_forever()

# if __name__ == '__main__':
#     broker = '161.200.84.240'
#     port = 1883
#     initial_topic = "/mqtt/testOn"
#     mqtt_subscriber = MqttSubscriber(broker, port, initial_topic)
#     mqtt_subscriber.add_subscription("new_topic_to_subscribe")
#     mqtt_subscriber.run()


