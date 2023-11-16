import random
import time
from paho.mqtt import client as mqtt_client

class MqttPublisher:
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'publish-{random.randint(0, 1000)}'
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self):
        msg_count = 1
        while True:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = self.client.publish(self.topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1

    def run(self):
        self.client.loop_start()
        self.publish()
        self.client.loop_stop()

if __name__ == '__main__':
    broker = 'broker.emqx.io'
    port = 1883
    topic = "python/mqtt"
    # topic = "new_topic_to_subscribe"
    mqtt_publisher = MqttPublisher(broker, port, topic)
    mqtt_publisher.run()
