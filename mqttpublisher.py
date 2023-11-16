import time
from paho.mqtt import client as mqtt_client
from mqttsubscriber import MqttSubscriber

class MqttPublisher:
    def __init__(self, broker, port, topic, username, password):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_username = username
        self.client_password = password
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    # def pub_function1(self):
    #     msg_count = 1
    #     while msg_count<10:
    #         time.sleep(1)
    #         msg = f"messages: {msg_count}"
    #         result = self.client.publish(self.topic, msg)
    #         status = result[0]
    #         if status == 0:
    #             print(f"Send `{msg}` to topic `{self.topic}`")
    #         else:
    #             print(f"Failed to send message to topic {self.topic}")
    #         msg_count += 1
        

    # def run(self):
    #     self.client.loop_start()
    #     self.pub_function1()
    #     self.client.loop_stop()

# if __name__ == '__main__':
#     broker = "161.200.84.240"
#     port = 1883
#     username = "cps"
#     password = "21035350"
#     topic = "/mqtt/testOn"
#     mqtt_publisher = MqttPublisher(broker, port, topic, username, password)
#     mqtt_publisher.run()
