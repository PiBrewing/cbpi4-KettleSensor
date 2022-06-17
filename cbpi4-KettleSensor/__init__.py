
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.config import ConfigType
from cbpi.api.dataclasses import Kettle, Props, Step, Fermenter
from cbpi.api.property import Property, PropertyType
from cbpi.api.base import CBPiBase

logger = logging.getLogger(__name__)

@parameters([Property.Kettle(label="Kettle"),
             Property.Select(label="Data",options=["TargetTemp","Power"],description="Select kettle data to be monitored")])
class KettleSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(KettleSensor, self).__init__(cbpi, id, props)
        self.value = self.value_old = 0
        self.kettle_controller : KettleController = cbpi.kettle
        self.kettle_id=self.props.get("Kettle")
        self.SensorType=self.props.get("Data","TargetTemp")
        self.log_data(self.value)


    async def run(self):
        value=0
        counter = 15 # equal to  ~ 30 seconds with sleep(2)
        while self.running is True:
            try:
                self.kettle = self.kettle_controller.get_state()
            except:
                self.kettle = None
            if self.kettle is not None:
                for kettle in self.kettle['data']:
                    if kettle['id'] == self.kettle_id:
                        if self.SensorType == "TargetTemp":
                            current_value = int(kettle['target_temp'])
                            value = current_value
                        else:
                            heater = kettle['heater']
                            kettle_heater = self.cbpi.actor.find_by_id(heater)
                            try:
                                state=kettle_heater.instance.state
                            except:
                                state = False
                            if state == True:
#                                logging.info("Instance: {}".format(state))
#                                logging.info(kettle_heater)
                                value = int(kettle_heater.power)

                        if counter == 0:
                            if value != 0:
                                self.value=value
                                self.log_data(self.value)
                                self.push_update(self.value)
                                self.value_old=self.value
                            counter = 15
                        else:
                            if value != self.value_old:
                                self.value=value
                                self.log_data(self.value)
                                self.push_update(self.value)
                                self.value_old=self.value
                                counter = 15
            self.push_update(self.value,False)
            #self.cbpi.ws.send(dict(topic="sensorstate", id=self.id, value=self.value))
            counter -=1
            await asyncio.sleep(2)
    
    def get_state(self):
        return dict(value=self.value)

@parameters([Property.Fermenter(label="Fermenter"),
             Property.Select(label="Data",options=["TargetTemp","Power"],description="Select kettle data to be monitored")])

class FermenterSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(FermenterSensor, self).__init__(cbpi, id, props)
        self.value = self.value_old = 0
        self.fermenter_controller : FermentationController = cbpi.fermenter
        self.fermenter_id=self.props.get("Fermenter")
        self.SensorType=self.props.get("Data","TargetTemp")



    async def run(self):
        value = 0
        counter = 15 # equal to  ~ 30 seconds with sleep(2)
        while self.running is True:
            try:
                self.fermenter = self.fermenter_controller.get_state()
            except:
                self.fermenter = None
            if self.fermenter is not None:
                for fermenter in self.fermenter['data']:
                    if fermenter['id'] == self.fermenter_id:
                        if self.SensorType == "TargetTemp":
                            current_value = float(fermenter['target_temp'])
                            value = current_value
                        else:
                            heater = fermenter['heater']
                            cooler = fermenter['cooler']
                            fermenter_heater = self.cbpi.actor.find_by_id(heater)
                            fermenter_cooler = self.cbpi.actor.find_by_id(cooler)
                            try:
                                state_h=fermenter_heater.instance.state
                            except:
                                state_h = False
                            try:
                                state_c=fermenter_cooler.instance.state
                            except:
                                state_c = False
                            if state_h == True:
                                value = 1
                            elif state_c == True:
                                value = -1
                            else:
                                value = 0

                        if counter == 0:
                            self.value=value
                            self.log_data(self.value)
                            self.push_update(self.value)
                            self.value_old=self.value
                            counter = 15
                        else:
                            if value != self.value_old:
                                self.value=value
                                self.log_data(self.value)
                                self.value_old=self.value
                                self.push_update(self.value)
                                counter = 15

            self.push_update(self.value,False)
            #self.cbpi.ws.send(dict(topic="sensorstate", id=self.id, value=self.value))
            counter -=1
            await asyncio.sleep(2)
    
    def get_state(self):
        return dict(value=self.value)

def setup(cbpi):
    cbpi.plugin.register("KettleSensor", KettleSensor)
    cbpi.plugin.register("FermenterSensor", FermenterSensor)
    pass
