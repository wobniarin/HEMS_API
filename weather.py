# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:21:30 2020

@author: adria.bove
"""

#http://api.openweathermap.org/data/2.5/forecast?lat=41.277194&lon=1.298196&appid=5b34e9090c043659ac6518294ffdca96&lang=ca
#http://api.openweathermap.org/data/2.5/weather?lat=41.277194&lon=1.298196&appid=5b34e9090c043659ac6518294ffdca96&lang=ca
#http://api.openweathermap.org/data/2.5/lat=41.277194&lon=1.298196&appid=5b34e9090c043659ac6518294ffdca96&lang=ca
from credentials import APPID,CP,country
import requests
from datetime import datetime
from BBDD import BBDD


class weather:
    def __init__(self):
        self.appid=APPID
        self.CP=CP
        self.country=country
        
    def gen_req(self,header):
        base_URL='http://api.openweathermap.org/data/2.5/'
        header=header+'?'
        location='lat=41.277194&lon=1.298196'
        token='&appid='+self.appid
        language='&lang=ca'
        
        
        url=base_URL+header+location+token+language
        response = requests.get(url)
        return response.json()
        
        
        
    def fore_w_req(self):
        response=self.gen_req('forecast')
        
        

        
        params=[]
        departments=[]
        cnt=response['cnt']
        data=[]
        for k in range(cnt):
            a=[a for a in response['list'][k]]
            for j in a:
                
                if j == 'dt':
                    params=params+[self.unix2time(response['list'][k][j],response['city']['timezone'])]
                    departments=departments+['dt']
                    
                elif j=='weather':
                    department=[department for department in response['list'][k][j][0]]
                    params=params+[response['list'][k][j][0][i] for i in department]
                    departments=departments+[j+" "+department for department in response['list'][k][j][0]]
                    
                elif j=='dt_txt':
                    pass
                    
                else:
                    department=[department for department in response['list'][k][j]]
                    params=params+[response['list'][k][j][i] for i in department]
                    departments=departments+[j+" "+department for department in response['list'][k][j]]
                    
            data=data+[dict(zip(departments, params))]
            
        self.store_data(data,'forecast_weather_BBDD')
        return data
    
    def current_w_req(self):
        response=self.gen_req('weather')
        
        params=[]
        departments=[]
        data=[]
        
        a=[a for a in response]
        for j in a:
            
            if j == 'visibility':
                params=params+[response[j]]
                departments=departments+['visibility']
                
            elif j=='weather':
                department=[department for department in response[j][0]]
                params=params+[response[j][0][i] for i in department]
                departments=departments+[j+" "+department for department in response[j][0]]
                
            elif j in ['dt_txt','base','timezone','id','name','cod']:
                pass
                
            elif j== 'dt':
                params=params+[self.unix2time(response[j],response['timezone'])]
                departments=departments+['dt']
                
            else:
                department=[department for department in response[j]]
                params=params+[response[j][i] for i in department]
                departments=departments+[j+" "+department for department in response[j]]
                
        data=data+[dict(zip(departments, params))]
            
        self.store_data(data,'current_weather_BBDD')
        return data
        
    def store_data(self,data,name):
        this_BBDD=BBDD(name)
        this_BBDD.store_data(data)   
    
    def cur_w_parameters(self):
        pass
    def fore_w_parameters(self):
        pass

    def unix2time(self,string,timezone):
        ts = int(string)+int(timezone)
        dt= datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')


if __name__=='__main__':
    #define the objectin a variable
    wth_call=weather()

    #save the data in list(dict) format inside 2 variables
    forecast=wth_call.fore_w_req()
    #data=wth_call.current_w_req()
    
    #get the response in JSON format
    forecast_response=wth_call.gen_req('forecast')
    #current_response=wth_call.gen_req('weather')
    
    
    
    



