from paho.mqtt import client as mqtt_client
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
        self.client = MqttPublisher.connect_mqtt(self)

    def pub_function1(self):     
        msg_count = 1
        while msg_count<10:
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = self.client.publish(self.topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1

    def run_topic(self):
        print("q")
        while True:
            mqtt_subscriber = MqttSubscriber(self.broker, self.port, self.topic)
            mqtt_subscriber.add_subscription("new_topic_to_subscribe")
            mqtt_subscriber.client.loop_start()
            client = MqttSubscriber.connect_mqtt(self)
            receive_msg = MqttSubscriber.on_message(self, client, userdata, msg)
            if receive_msg  == self.topic:
                print('Hi', receive_msg)
                mqtt_publisher = MqttPublisher(broker, port, topic, username, password)
                mqtt_publisher.pub_function1()
            mqtt_subscriber.client.loop_stop()
   
            
    
if __name__ == '__main__':
    broker = '161.200.84.240'
    port = 1883
    initial_topic = "/mqtt/testnun"
    username = "cps"
    password = "21035350"
    topic = "/mqtt/testnun"
    a = Action(broker, port, topic, username, password)
    a.run_topic()



# #sub
# if __name__ == '__main__':
#     broker = '161.200.84.240'
#     port = 1883
#     initial_topic = "/mqtt/testOn"
#     mqtt_subscriber = MqttSubscriber(broker, port, initial_topic)
#     mqtt_subscriber.add_subscription("new_topic_to_subscribe")
#     mqtt_subscriber.run()

# #pub
# if __name__ == '__main__':
#     broker = "161.200.84.240"
#     port = 1883
#     username = "cps"
#     password = "21035350"
#     topic = "/mqtt/testOn"
#     mqtt_publisher = MqttPublisher(broker, port, topic, username, password)
#     mqtt_publisher.run()
