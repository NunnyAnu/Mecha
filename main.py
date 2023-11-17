from mqttsubscriber import MqttSubscriber
from mqttpublisher import MqttPublisher
import time
from pypylon import pylon
from pymongo import MongoClient
import cv2
from bson import Binary
import numpy as np

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

        self.image = np.full((2064, 3088, 3), (255, 255, 255), dtype=np.uint8)
        self.checkcam = False
        self.capcount = 0

        self.CONNECTION_STRING = 'mongodb+srv://mechatronics:BhamAomNunEarn@dimension.i10gagw.mongodb.net/'
        self.client = MongoClient(self.CONNECTION_STRING)
        self.Database = self.client['Dimension']
        self.Collection = self.Database['Captured']
        self.Collection2 = self.Database['Preprocessed_Image']

        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

        new_width = self.camera.Width.Value - self.camera.Width.Inc
        if new_width >= self.camera.Width.Min:
            self.camera.Width.Value = new_width

        self.numberOfImagesToGrab = 2
        self.camera.StartGrabbingMax(self.numberOfImagesToGrab)

    def resetGrabbingMax(self):
        self.numberOfImagesToGrab += 1
        self.camera.StartGrabbingMax(self.numberOfImagesToGrab)

    def pubpub(self, message):
        msg = message
        result = self.mqtt_publisher.client.publish(self.pub_topic, msg)

    def on_message(self, client, userdata, msg):
        receive_msg = msg.payload.decode()
        if receive_msg == 'isOn':
            res = self.checkcamera()
            if res:
                feedback = 'on'
                self.pubpub(feedback)
            else:
                feedback = 'off'
                self.pubpub(feedback)
        
        elif receive_msg == 'isTaken':
            if not self.checkcamera():
                self.pubpub('Please Initalize the camera')
                return
            cap = self.capture()
            self.image = self.preprocessimage(cap)
            doc_count = self.Collection.count_documents({})
            self.publishtodb(self.image, 1)
            while self.Collection.count_documents({}) == doc_count:
                time.sleep(0.01)
            feedback = 'Captured'
            self.capcount += 1
            self.pubpub(feedback)
            self.resetGrabbingMax()

        elif receive_msg == 'isProcessed':
            if self.capcount == 0:
                self.pubpub('The image has not yet taken')
                return
            doc_count = self.Collection.count_documents({})
            self.publishtodb(self.image, 1)
            while self.Collection.count_documents({}) == doc_count:
                time.sleep(0.01)
            feedback = 'Processed'
            self.pubpub(feedback)   

    def run_topic(self):
        print("Starting subscriber...")
        self.mqtt_subscriber.client.on_message = self.on_message

    def run(self):
        self.mqtt_subscriber.client.loop_forever()

    def checkcamera(self):
        if self.camera.IsGrabbing():
            self.checkcam = True
            return True
        else:
            self.checkcam = False
            return False
        
    def capture(self):
        grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            img = grabResult.Array
            print(img.shape)
        grabResult.Release()
        return img

    def preprocessimage(self, image):
        gray_image = image
        mean = np.mean(gray_image)
        median = cv2.medianBlur(gray_image, 3)
        bin_image = cv2.threshold(median, 0.75*mean, 255, cv2.THRESH_BINARY)
        self.publishtodb(bin_image[1], 1)
        return bin_image[1]

    def publishtodb(self, image, collection):
        if collection == 1:
            collection = self.Collection
        else:
            collection = self.Collection2
        image_binary = Binary(cv2.imencode('.jpg', image)[1].tobytes())
        data = {
            '_id': collection.count_documents({})+1,
            'img_binary' : image_binary
        }
        self.Collection.insert_one(data)
        return True

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
