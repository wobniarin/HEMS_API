# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 10:34:05 2020

@author: adria.bove
"""

#http://192.168.1.143/solar_api/v1/GetPowerFlowRealtimeData.fcgi
#http://192.168.1.143/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData

import requests
from searchIP import searchIPfronius
from BBDD import BBDD
from datetime import datetime

class fr_inverter():
    def __init__(self):
        sIP=searchIPfronius()
        sIP.buscador()
        self.inv_IP=sIP.ip_inversor

    def check_ip(self):
        pass
    
    
    def search_ip(self):
        pass
    
    
    
    def request(self, archive):
        
        if archive == 'FlowRT':
            
            try:   
                endpoint='http://'+self.inv_IP+'/' 
                get_archives='solar_api/v1/GetPowerFlowRealtimeData.fcgi'
                response = requests.get(url = endpoint+get_archives)
                return response
            except:
                print('NO ENS HEM CONNECTAT')
        
        elif archive == 'InverterRT':
            try:   
                endpoint='http://'+self.inv_IP+'/solar_api/' 
                version='v1/'
                get_archives='GetInverterRealtimeData.cgi?'
                scope='Scope=Device&'
                scopeid='DeviceId=1&'
                datacollection='DataCollection=CommonInverterData'
                response = requests.get(url = endpoint+version+'/'+get_archives+scope+scopeid+datacollection)
                return response
            except:
                print('NO ENS HEM CONNECTAT')
    
    def formating(self, objecte, process: str='W2kW'):
        if process=='W2kW':
            if objecte != None:
                objecte=objecte/1000
                return objecte
    
    def power_flows(self):
        response=self.request('FlowRT')
        response=response.json()
        P_PV=self.formating(response['Body']['Data']['Site']['P_PV'])
        P_grid=self.formating(response['Body']['Data']['Site']['P_Grid'])
        P_load=self.formating(response['Body']['Data']['Site']['P_Load'])
        P_Akku=self.formating(response['Body']['Data']['Site']['P_Akku'])
        dt=datetime.strptime(response['Head']['Timestamp'][0:19], '%Y-%m-%dT%H:%M:%S')
        
        data=[dict(zip(['dt','P_PV [kW]', 'P_grid [kW]', 'P_load [kW]','P_Akku [kW]'],[dt,P_PV, P_grid, P_load,P_Akku]))]
        
        return data
    
    def P_grid(self):
        response=self.request('FlowRT')
        response=response.json()
        P_grid=self.formating(response['Body']['Data']['Site']['P_Grid'])
        return P_grid
    
    def P_PV(self):
        response=self.request('FlowRT')
        response=response.json()
        P_PV=self.formating(response['Body']['Data']['Site']['P_PV'])
        return P_PV    
    
    def P_load(self):
        response=self.request('FlowRT')
        response=response.json()
        P_load=self.formating(response['Body']['Data']['Site']['P_Load'])
        return P_load
    
    def grid_data(self):
        PF_data=self.power_flows()
        response=self.request('InverterRT')
        response=response.json()
        try:
            F_AC=response['Body']['Data']['FAC']['Value']
        except:
            F_AC=None
        try:
            I_AC=response['Body']['Data']['IAC']['Value']
        except:
            I_AC=None
        try:
            U_AC=response['Body']['Data']['UAC']['Value']
        except:
            U_AC=None
        try:
            I_DC=response['Body']['Data']['IDC']['Value']
        except:
            I_DC=None
        try:
            U_DC=response['Body']['Data']['UDC']['Value']
        except:
            U_DC=None
        
        data=[{'Frequency [Hz]':F_AC, 'AC current [A]':I_AC, 'AC voltage [V]':U_AC, 'DC current [A]':I_DC, 'DC voltage [V]':U_DC}]
        PF_data[0].update(data[0])
        self.store_data(PF_data,'grid_BBDD')
        
        return PF_data
    
    
    def store_data(self,data,name):
        this_BBDD=BBDD(name)
        this_BBDD.store_data(data)
    
  
if __name__ == '__main__':   
    
    #First we create the object which is the inverter places in Puig and I'll call it fr_puig (Fronius Puig)
    fr_puig=fr_inverter()
    
    recalcular='y'
    while recalcular=='y': 
        #to get the data of the power flows exist several methods to use power_flows() give them in a tuple and kW
        #exist also methods for the single values this difference is important because calling all together ensures they are in the same instant
        
        P=fr_puig.power_flows()
        
        consum=fr_puig.P_load()
        p_PV=fr_puig.P_PV()
        intercanvi_xarxa=fr_puig.P_grid()
        
        print("Ara estàs consumint "+str(consum)+" kW")
        print("Les teves plaques generen "+str(p_PV)+" kW")
        if intercanvi_xarxa<0:
            print("Per tant a la xarxa hi van "+str(-intercanvi_xarxa)+" kW")
        else:
            print("Per tant estas agafant de la xarxa "+str(intercanvi_xarxa)+" kW")
        #to get the status of the grids of the household the inverter and its sensosrs provides the frequency and voltages
        #the method returns the values in a dict 
        grid_status=fr_puig.grid_data()
        recalcular=input("Escriu 'y' i prem enter per recalcular: ")
        print()
        print()
        
        #to extract the value use:
        #print(grid_status['Frequency']['Value'])
        #print(grid_status['AC current']['Value'])
        #print(grid_status['AC voltage']['Value'])
        #print(grid_status['DC current']['Value'])
        #print(grid_status['DC voltage']['Value'])

