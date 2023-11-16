from mqttsubscriber import MqttSubscriber
from mqttpublisher import MqttPublisher
import time

class Action:
    def __init__(self, broker, port, subscribing_topic, publishing_topic, username, password):
        self.broker = broker
        self.port = port
        self.sub_topic = subscribing_topic
        self.pub_topic = publishing_topic
        self.client_username = username
        self.client_password = password
        self.mqtt_subscriber = MqttSubscriber(self.broker, self.port, self.sub_topic)
        self.mqtt_publisher = MqttPublisher(self.broker, self.port, self.pub_topic, self.client_username, self.client_password)

    def pub_function1(self, msg):
        # msg_count = 1
        # while msg_count < 10:
            # time.sleep(1)
        msg = f"{msg}"
        result = self.mqtt_publisher.client.publish(self.pub_topic, msg)
            # status = result.rc
            # if status == 0:
            #     print(f"Send `{msg}` to topic `{self.topic}`")
            # else:
            #     print(f"Failed to send message to topic {self.pub_topic}")
            # msg_count += 1

    def on_message(self, client, userdata, msg):
        receive_msg = msg.payload.decode()
        # print(f"Received message: {receive_msg} on topic: {msg.topic}")
        

    def run_topic(self):
        print("Starting subscriber...")
        self.mqtt_subscriber.client.on_message = self.on_message
        # self.mqtt_subscriber.client.loop_start()
        time.sleep(2)  # Wait for the subscriber to establish connection
        # print("Starting publisher...")
        # self.pub_function1('Hello')
        # self.mqtt_subscriber.client.loop_stop()

    def run(self):
        self.mqtt_subscriber.client.loop_forever()


if __name__ == '__main__':
    broker = '161.200.84.240'
    port = 1883
    sub_topic = "/mqtt/toPi1"
    pub_topic = '/mqtt/fromPi1'
    username = "cps"
    password = "21035350"
    a = Action(broker, port, sub_topic, pub_topic, username, password)
    a.run_topic()
    a.run()
