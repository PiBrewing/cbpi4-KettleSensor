
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *

logger = logging.getLogger(__name__)

@parameters([Property.Kettle(label="Kettle")])
class CustomSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(CustomSensor, self).__init__(cbpi, id, props)
        self.value = 0
        self.kettle_controller : KettleController = cbpi.kettle
        self.kettle_id=self.props.get("Kettle")
        logging.info(self.kettle_id)
        self.value_old = self.value
        self.log_data(self.value)
        self.push_update(self.value)


    async def run(self):
        counter = 15 # equal to  ~ 30 seconds with sleep(2)
        while self.running is True:
            try:
                self.kettle = self.kettle_controller.get_state()
            except:
                self.kettle = None
            if self.kettle is not None:
                for kettle in self.kettle['data']:
                    if kettle['id'] == self.kettle_id:
                        current_value = int(kettle['target_temp'])
                        self.value = current_value
#                        logging.info("Counter: {} | Value: {}".format(counter,self.value))
                        if counter == 0:
                            if self.value != 0:    
                                self.log_data(self.value)
                            counter = 15
                        else:
                            if self.value != self.value_old:
                                self.log_data(self.value)
                                self.value_old=self.value
                                counter = 15

                        self.push_update(self.value)
            counter -=1
            await asyncio.sleep(2)
    
    def get_state(self):
        return dict(value=self.value)

def setup(cbpi):
    cbpi.plugin.register("TargetTempSensor", CustomSensor)
    pass
