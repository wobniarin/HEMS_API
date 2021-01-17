# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:54:26 2020

@author: adria.bove
"""

#https://api.esios.ree.es/application/json/api.esios.ree.es/Token token=\

import credentials
import datetime as dt
import requests
import matplotlib.pyplot as plt
from BBDD import BBDD

class PVPC_prices:
    def __init__(self,tariff: str='VHC'): #2.0A 2.0DHA 2.0DHS 'GEN' 'NOC' 'VHC'
        self.tariff=tariff
        self.tokenREE=credentials.tokenREE

    def request(self):

        endpoint='https://api.esios.ree.es/'
        headers = {'Accept': 'application/json',
                   'Host': 'api.esios.ree.es',
                   'Authorization': 'Token token=\' self.tokenREE'
                   }
        params = {'date': self.date}
        get_archives='/archives/66/download_json?locale=es'
        self.response = requests.get(url = endpoint+get_archives, params = params, headers = headers)

        return self.response.json()

    def formating(self,objecte,size):
        if size=='1':
            objecte=float(objecte.replace(',', '.'))*0.001
            return objecte
    
    def hour_price(self, hora: int=int(dt.datetime.now().strftime('%H')), day_from_today: int=0):
        self.date=str(dt.date.today()+dt.timedelta(days=day_from_today))
        try:
            response=self.request()
            hourprice=response['PrecioFinal'][hora][self.tariff]
            return self.formating(hourprice,'1')
        except:
            return 0.09

    def day_prices(self,day_from_today: int=0, ndays: int=1):
        dayprices=[[self.hour_price(hora,day_from_today+day) for hora in range(24)] for day in range(ndays)]
        

        dtdays=[dt.datetime.combine(dt.date.today()+dt.timedelta(days=day_from_today)+dt.timedelta(days=day), dt.datetime.min.time()) for day in range(ndays)]
        data=[]
        for i in range(ndays):
            data=data+[dict(zip(['dt']+list(range(24)),[dtdays[i]]+dayprices[i]))]
        self.store_data(data,'REE_BBDD')
        return data
    
    def store_data(self,data,name):
        this_BBDD=BBDD(name)
        this_BBDD.store_data(data)
    

    def plot_prices(self,object):
        llista=[]
        try :
            len(object[0])
            for i in range(len(object)):
                piece=[]
                for a in range(len(object[i])):
                    piece=piece + [object[i][a]]
                llista=llista+piece
        except:
            llista=object
            
        plt.plot(llista)
        


if __name__ == '__main__':
    
    # to use this module first import the module
    # from PVPC_prices import PVPC_prices
    
    #next declare the objects which usually are the three tariffs:
    PVPC_2A = PVPC_prices('GEN')
    PVPC_2DHA = PVPC_prices('NOC')
    PVPC_2DHS = PVPC_prices('VHC') #OR PVPC_2DHS = PVPC_prices()
    
    #next ask for the prices in the desired format
    
    #to know the price at a specific hour and day in € use:
    print(PVPC_2DHS.hour_price())
    #preu=PVPC_2DHS.hour_price(8,0)
    
    
    #to know the prices of a complete day use:
    preus_dia=PVPC_2DHS.day_prices()
    
    #to get the prices for a range of days use: first argument the initial day, if yesterday use -1, today 0 and tomorrow 1. Can reat from -9 to 1. 
    #the second argument the number of days you want
    #preus_dies=PVPC_2DHS.day_prices(-1,2)
    
    #to plot the results
    #PVPC_2DHS.plot_prices(preus_dies)
    #PVPC_2DHS.plot_prices(preus_dia)
    
    
    
    
    