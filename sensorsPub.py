import sys
import RPi.GPIO as GPIO
from time import sleep
import threading
import os
import logging
from datetime import datetime
import Adafruit_DHT


logging.basicConfig(level=logging.INFO)

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE") #These have to be set up as environment variables inside Pi
pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH") #These have to be set up as environment variables inside Pi
pnconfig.uuid = '02060d4f-508a-4ca2-b1d2-a1d22ee5cc48' #
pubnub = PubNub(pnconfig)

my_channel = "tadas-pi-channel"
data = {}
publish_message = {}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

soil = 40
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_BCM_PIN = 15 #USE BCM NUMBERING FOR THIS
ldr = 3
led = 16


GPIO.setup(soil,GPIO.IN)
GPIO.setup(ldr,GPIO.IN)
GPIO.setup(led,GPIO.OUT)


def call_sensors():
      print()
      check_temp(5)
      check_soil(5)
      check_for_light(5)
      publish_to_pub()
      sleep(5)


#test dht22 for 10 seconds
def check_temp(seconds):
      global publish_message
      for i in range(seconds):
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_BCM_PIN)
            
      if humidity is not None and temperature is not None:
            publish_message.update({"temperature" : "{:.1f}".format(temperature), "humidity": "{:.1f}".format(humidity)})
      else:
            publish(my_channel, {"fail" : "Fail to retrieve data"})
      sleep(0.2)

def check_soil(seconds):
      global publish_message
      soil_status = "Dry"
      for i in range(seconds):
            if not(GPIO.input(soil)):
                  soil_status = "Wet"
            else:
                  soil_status = "Dry"
            sleep(0.2)
      publish_message.update({"soil":soil_status})

#test ldr with led
def check_for_light(seconds):
      global publish_message
      brightness_levels = "Light"
      for i in range(seconds):
        if GPIO.input(ldr):
            brightness_levels = "Dark"
            GPIO.output(led,True)
        else:
            brightness_levels = "Light"
            GPIO.output(led,False)
        sleep(0.2)
      publish_message.update({"brightness":brightness_levels})

      

def publish_to_pub():
    global publish_message
    now = datetime.now()
    current_time = now.strftime("%d-%M-%Y %H:%M")
    publish_message.update({"time":current_time})
    publish(my_channel, publish_message)


def publish(channel, msg):
    pubnub.publish().channel(my_channel).message(msg).pn_async(my_publish_callback)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        #print("message success published")
        pass  # Message successfully published to specified channel.
    else:
        print("message failed publish")
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            print("success connected to PubNub")
            pubnub.publish().channel(my_channel).message('Raspberry Pi Connected').pn_async(my_publish_callback)
            sleep(1)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    # When a message goes out and comes this get triggered and can be used to call events based off the messages
    def message(self, pubnub, message):
        # Handle new message stored in message.message
        try:
            print(message.message, ": ", type(message.message))
            msg = message.message
            key = list(msg.keys())
            if key[0] == "event":
                self.handle_event(msg)
        except Exception as ex:
            print(message.message)
            print(ex)
            pass


    def handle_event(self, msg):
        global data
        event_data= msg["event"]
        if "refresh" == event_data:
            call_sensors()

if __name__ == '__main__':
    sensors_thread = threading.Thread(target = call_sensors)
    sensors_thread.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()