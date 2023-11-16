from mqttsubscriber import MqttSubscriber
import random

if __name__ == '__main__':
    broker = 'broker.emqx.io'
    port = 1883
    client_id = f'subscribe-{random.randint(0, 100)}'
    initial_topic = "python/mqtt"
    mqtt_subscriber = MqttSubscriber(broker, port, initial_topic)
    mqtt_subscriber.add_subscription("new_topic_to_subscribe")
    mqtt_subscriber.run()

# broker = 'broker.emqx.io'
# port = 1883
# initial_topic = "python/mqtt"
# mqtt_subscriber = MqttSubscriber(broker, port, initial_topic)
# mqtt_subscriber.add_subscription("new_topic_to_subscribe")
# mqtt_subscriber.run()