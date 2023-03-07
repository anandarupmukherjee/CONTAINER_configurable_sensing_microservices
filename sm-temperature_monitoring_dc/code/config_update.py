import paho.mqtt.client as mqtt
import os
import json
import time






def on_message_config(mosq, obj, msg):
    print("entered loop")
    top=msg.topic
    print(top)
    data = "{}".format(str(msg.payload,"utf-8"))
    data1=json.loads(data)

    tdata={
        "machine":{
            "name": data1["Location"],
        },
        "sensing":{
            "adc": data1["Sensor"],
        },
        "threshold":{
            "t1": data1["Threshold"],
        }
    }

    with open('/app/config.txt', 'w') as convert_file:
        convert_file.write(json.dumps(tdata))
        # time.sleep(10)









print("Edge handshake initiate...")
mqttc = mqtt.Client()
print("Done. Listening on the local network....")

# Add message callbacks that will only trigger on a specific subscription match.

mqttc.message_callback_add("config/t1", on_message_config)
mqttc.connect("172.18.0.4", 1883, 60)
mqttc.subscribe("config/#", 0)

mqttc.loop_forever()
print('Publish End')
