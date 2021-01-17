# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:07:58 2020

@author: adria.bove
"""

from datetime import datetime, timedelta
from BBDD import BBDD
from PVPC_prices import PVPC_prices
from weather import weather
import nissanapi
from fr_inverter import fr_inverter
from PV_model_singlediode import PV
from credentials import num_panels
from forecaster import consumption

class datacall:
    def __init__(self):
        
        
        
        self.num_panels=num_panels
        
        
        
        self.calls=['forecast_weather_BBDD','car_BBDD','grid_BBDD','REE_BBDD','PV_forecast_BBDD','current_weather_BBDD','loads_forecast','PV_corr_forecast_BBDD']
        
        self.freq=[timedelta(days=1),timedelta(minutes=15),timedelta(seconds=10),timedelta(days=1),timedelta(days=1),timedelta(minutes=10),timedelta(days=1),timedelta(days=1)]
        
        self.offset=[timedelta(days=-5),timedelta(days=0),timedelta(days=0),timedelta(days=0),timedelta(days=-5),timedelta(days=0),timedelta(days=-5),timedelta(days=0)]
    
    def caller(self):
        self.now=datetime.now()        
        ide=-1
        for i in self.calls:
            ide=ide+1
            BBDD_=BBDD(i)
            if BBDD_.check_BBDD_exists()==1:   
                last_entry_time=BBDD_.last_entry_time()
                flag=0
            else:
                flag=1
            
            if ((self.now-last_entry_time.replace(tzinfo=None)-self.offset[ide])>self.freq[ide]) | flag==1:
                self.weather(ide)
                self.nissan(ide)
                self.inverter(ide)
                self.REE(ide)
                self.PV_forecast(ide)
                self.current_weather(ide)
                self.consumption_forecast(ide)
                self.PV_corr_forecast(ide)
                
    
    def weather(self,ide):
        if ide==0:
            try:
                wth_call=weather()
                wth_call.fore_w_req()
                print('weather actualitzat')
            except:
                print('weather error connexió')
    def nissan(self,ide):
        if ide==1:
            try:
                nissan=nissanapi.car_data_recollect()
                nissan.data()
                print('car actualitzat')
            except:
                print('nissan error connexió')
    
    def inverter(self,ide):
        if ide==2:
            try:
                fr_puig=fr_inverter()
                fr_puig.grid_data()
                print('inverter actualitzat')
            except:
                print('inverter error connexió')
    
    def REE(self,ide):
        if ide==3:
            try:
                PVPC_2DHS = PVPC_prices('VHC') #OR PVPC_2DHS = PVPC_prices()
                PVPC_2DHS.day_prices()
                print('REE actualitzat')
            except:
                print('REE error connexió')
    
    def PV_forecast(self,ide):
        if ide==4:
            try:
                puig_pv=PV(num_panels=self.num_panels) 
                puig_pv.sim_PV_power(timestamp=15)
                print('PV actualitzat')
            except:
                print('PV error connexió')
    
    def current_weather(self,ide):
        if ide==5:
            try:
                wth_call=weather()
                wth_call.current_w_req()
                print('weather actualitzat')
            except:
                print('weather error connexió')    
                
    def consumption_forecast(self,ide):
        if ide==6:
            try:
                load_call=consumption('grid_BBDD')
                load_call.forecaster(timestamp=15)
                print('consumption forecast actualitzat')
            except:
                print('consumption forecast error connexió')  
                
    def PV_corr_forecast(self,ide):
        if ide==7:
            try:
                puig_pv=PV(num_panels=self.num_panels, corrected=1)
                puig_pv.sim_PV_power(timestamp=15)
                print('PV corrected actualitzat')
            except:
                print('PV corrected error connexió')   

    
if __name__=='__main__':
    self=datacall()
    self.caller()
    
    

