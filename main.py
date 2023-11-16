from mqttsubscriber import MqttSubscriber
from mqttpublisher import MqttPublisher
import time

class Action:
    def __init__(self, broker, port, topic, username, password):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.sub_topics = [topic]
        self.client_username = username
        self.client_password = password
        self.mqtt_subscriber = MqttSubscriber(self.broker, self.port, self.topic)
        self.mqtt_subscriber.add_subscription("new_topic_to_subscribe")
        self.mqtt_publisher = MqttPublisher(self.broker, self.port, self.topic, self.client_username, self.client_password)

    def pub_function1(self):
        msg_count = 1
        while msg_count < 10:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = self.mqtt_publisher.client.publish(self.topic, msg)
            status = result.rc
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1

    def on_message(self, client, userdata, msg):
        receive_msg = msg.payload.decode()
        print(f"Received message: {receive_msg} on topic: {msg.topic}")

    def run_topic(self):
        print("Starting subscriber...")
        self.mqtt_subscriber.client.on_message = self.on_message
        self.mqtt_subscriber.client.loop_start()
        time.sleep(2)  # Wait for the subscriber to establish connection
        print("Starting publisher...")
        self.pub_function1()
        self.mqtt_subscriber.client.loop_stop()


if __name__ == '__main__':
    broker = '161.200.84.240'
    port = 1883
    topic = "/mqtt/testnun"
    username = "cps"
    password = "21035350"
    a = Action(broker, port, topic, username, password)
    a.run_topic()
