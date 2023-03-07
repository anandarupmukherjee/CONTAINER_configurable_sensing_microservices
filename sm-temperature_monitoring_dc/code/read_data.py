# ----------------------------------------------------------------------
#
#    Power Monitoring (Basic solution) -- This digital solution measures,
#    reports and records both AC power and current consumed by an electrical 
#    equipment, so that its energy consumption can be understood and 
#    taken action upon. This version comes with one current transformer 
#    clamp of 20A that is buckled up to the electric line the equipment 
#    is connected to. The solution provides a Grafana dashboard that 
#    displays current and power consumption, and an InfluxDB database 
#    to store timestamp, current and power. 
#
#    Copyright (C) 2022  Shoestring and University of Cambridge
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ----------------------------------------------------------------------

import time
from smbus2 import SMBus
from mlx90614 import MLX90614
import os
from w1thermsensor import W1ThermSensor
import board
import digitalio
import logging
import tomli
import max6675
import adafruit_ahtx0
import paho.mqtt.client as mqtt
import json


logging.basicConfig(level=logging.DEBUG)  
logger = logging.getLogger("analysis.baseline");
logging.getLogger("matplotlib").setLevel(logging.WARNING)

# def get_config():
#     with open("/app/config/config.toml", "rb") as f:
#         toml_conf = tomli.load(f)
#     logger.info(f"config:{toml_conf}")
#     return toml_conf


def get_config():
    with open('/app/config.txt', 'r') as convert_file:
        toml_conf=json.loads(convert_file.read())
        return toml_conf


class MLX90614_temp:
    def __init__(self):
        self.bus = SMBus(1)
        self.sensor=MLX90614(self.bus,address=0x5a)

    def ambient_temp(self):
        return self.sensor.get_amb_temp()

    def object_temp(self):
        return self.sensor.get_obj_temp()
        


class W1Therm:
    def __init__(self):
        self.sensor = W1ThermSensor()
        

    def ambient_temp(self):
        return self.sensor.get_temperature()


class k_type:
    # https://github.com/archemius/MAX6675-Raspberry-pi-python/blob/master/temp_read_1_sensor.py
    def __init__(self):
        self.cs = 23
        self.sck = 24
        self.so = 25
        max6675.set_pin(self.cs, self.sck, self.so, 1) #[unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
        

    def ambient_temp(self):
        return max6675.read_temp(self.cs)



class aht20:
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_ahtx0.AHTx0(i2c)
        
    def ambient_temp(self):
        return self.sensor.temperature
        


def do_run(conf):
    
    machine_name = conf['machine']['name']
    
    Threshold = conf['threshold']['t1']                # User sets the threshold in the config file
    
    if conf['sensing']['adc'] == 'MLX90614_temp':
        adc = MLX90614_temp()
    elif conf['sensing']['adc'] == 'W1ThermSensor':
        adc = W1Therm()
    elif conf['sensing']['adc'] == 'K-type':
        adc = k_type()
    elif conf['sensing']['adc'] == 'AHT20':
        adc = aht20()
    else:
        raise Exception(f'ADC "{conf["sensing"]["adc"]}" not recognised/supported')
    
    
    #todo: error check on loaded in config
  
    while True:
        
        AmbientTemp = adc.ambient_temp()
        # ObjectTemp = adc.object_temp()
        if AmbientTemp > float(Threshold):
            AlertVal = 1
        else:
            AlertVal = 0

        logger.info(f"temperature_reading: {AmbientTemp}")
        var = "curl -i -XPOST 'http://172.18.0.2:8086/write?db=emon' --data '"+machine_name+" temp="+str(AmbientTemp)+",threshold="+str(Threshold)+",alertStatus="+str(AlertVal)+"'"
        os.system(var)
        time.sleep(1)


def run():
    conf = get_config()
    do_run(conf)

if __name__ == "__main__":
    run()
 