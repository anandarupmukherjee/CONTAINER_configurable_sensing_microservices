import os
import json
import paho.mqtt.client as mqtt
import time


print("Initiating transmission over MQTT")
mqttc = mqtt.Client()
print("Done. Listening on the local network....")

while(True):
    with open("./app/config.txt", "r") as f:
        dict_val=f.read()
        json_acceptable_string = dict_val.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        machine=d["Location"]
        adc=d["Sensor"]
        t1=d["Threshold"]
        print(t1)
        mqttc.connect('172.18.0.4', 1883, 60)
        mqttc.publish("config/t1",payload=json_acceptable_string)
        time.sleep(5)
        #print("Time transmitted to local network....")
        # mqttc.loop_forever()
        print('Publish End')

