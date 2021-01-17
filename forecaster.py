# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:58:57 2020

@author: adria.bove
"""

from BBDD import BBDD
import analytics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

class consumption:
    def __init__(self, nom):
        self.nom_BBDD=nom
    
    def forecaster(self,timestamp):
        self.timestamp=str(timestamp)
        # get the df
        this_BBDD=BBDD(self.nom_BBDD)
        a=pd.Series(dtype='float64')
        
        
        
        
        k=0
        list_weekdays=[(dt.datetime.now()+dt.timedelta(days=i+k)).weekday() for i in range(5)]
        for weekday in list_weekdays:
            df=this_BBDD.extract_weekday(weekday)
            
            #send it to the mean_day function que farà el dia tipus
            
            a=a.append(self.mean_day(df,k))
            k=k+1
        
        del(a[0])
        a['dt']=a.index
        a = a.reset_index(drop=True)
        
        self.store_data(a,'loads_forecast')
        
        return a
    
    def mean_day(self,df,k): #amb el weekday he de fer millor de date_range i fer-lo sobre el valor del timer
        df['timer'] = df.dt.apply(self.massive_rounder,groupsize=1,groups=int(60))
        
        df = df.rename(columns={'P_load [kW]': 'P_load'})
        df.P_load=pd.to_numeric(df.P_load)
        mean_DAY=df.groupby('timer').P_load.mean()
        mean_DAY=mean_DAY.to_frame()
        
        start_date=dt.datetime.combine(dt.date.today(), dt.datetime.min.time())#+dt.timedelta(days=1)
        mean_DAY['dta']=mean_DAY.index
        mean_DAY.dta=mean_DAY.dta.apply(lambda x: dt.timedelta(minutes=x) + start_date + dt.timedelta(days=k))
        mean_DAY.index=mean_DAY.dta
        del(mean_DAY['dta'])
        
        new_mean_DAY=mean_DAY.resample(self.timestamp+'T').pad()
        
        return new_mean_DAY

    
    def massive_rounder(self, element, groupsize, groups):
        
        for i in range(groups):
            if element.time().minute < (groupsize*(range(groups)[i]+1)):
                return range(groups)[i] + element.time().hour*groups
        
    
    def store_data(self,data,name):
        this_BBDD=BBDD(name)
        this_BBDD.store_data(data)   
        

if __name__ == '__main__':
    consumption_forecast=consumption('grid_BBDD')
    b=consumption_forecast.forecaster(timestamp=15)
    plt.plot(-b.P_load)