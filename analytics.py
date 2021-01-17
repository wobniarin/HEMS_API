# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 19:22:40 2020

@author: adria.bove

Llibreria per fer dibuixos de 

"""

# importing libraries 
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from BBDD import BBDD
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
import scores_metrics_diagnosis_tools as scores


class plotter:
    
    def lines(self, BBDDs, Columns, frequencies, y_label, title, legend, signs, days_from_today:int=-1, ndays:int=1, save:str='', input_df:list=[]):
    
        colors=['hotpink','cornflowerblue','green','purple','slateblue','firebrick']
        # defining color schemes
        plt.style.use('seaborn-whitegrid')
        
        if len(input_df)==0:
            dfs=[BBDD(i).extract(days_from_today,ndays) for i in BBDDs]
            for i in range(len(dfs)):
                dfs[i].index=dfs[i]['dt']
        else:
            dfs=input_df
        
        
        
        # data visualization 
        # defininig figure size 
        
        a=plt.figure(figsize=(15,10))
        
        k=0
        curves=[]
        for i in range(len(dfs)):
            for j in Columns:
                try:
                    ys=pd.to_numeric(dfs[i][j]).resample(str(frequencies[k])+'T').mean()
                    # plotting some lines 

                    plt.plot(ys.index, signs[k]*ys, label=legend[k], color= colors[k], figure=a)
                    k=k+1
                    curves=curves+ys
                except:
                    pass
        
        # setting limits to x axes 
        plt.xlim([dt.date.today()+dt.timedelta(days=days_from_today), dt.date.today()+dt.timedelta(days=days_from_today+ndays)])
        
        # including legend on the plot 
        plt.legend()
        # x axis label 
        plt.xlabel("Time [h]")
        # y axis label 
        plt.ylabel(y_label)
        # setting title 
        date_range=' from '+str(dt.date.today()+dt.timedelta(days=days_from_today))+' to '+str(dt.date.today()+dt.timedelta(days=days_from_today+ndays));
        plt.title(title+date_range)
        
        if save!='':
        # Saving figure 
            plt.savefig(save+".png", dpi=200)
        # Show plot
        

        plt.show()

        
        return a
        #self.ytrue=curves[0]
        #self.ypred=curves[1]
        
        #print(self.bias())
        
        #return [self.forecast_error(),self.MAPE(),self.RMSE(),self.bias()]
    
 
class scoring:
    #def lines(self, BBDDs, Columns, frequencies, y_label, title, legend, signs, days_from_today:int=-1, ndays:int=1, save:str=''):
    def some_scores(self, BBDDs, Columns, frequencies, signs, days_from_today:int=-1, ndays:int=1, y_label:str='', title:str='Scoring graph', legend:list=['Real','Forecasted'], save:str=''):
        
        dfs=[BBDD(i).extract(days_from_today,ndays) for i in BBDDs]
        
        for i in range(len(dfs)):
            dfs[i].index=dfs[i]['dt']
            
        curves=[pd.to_numeric(dfs[i][Columns[i]]).resample(str(frequencies)+'T').pad().to_frame()*signs[i] for i in range(2)]
        
        curves_df=curves[0].join(curves[1],lsuffix='a')
        if Columns[0]==Columns[1]:
            Columns=[Columns[0],Columns[1]+'a']
        curves_df=curves_df.dropna()
        curves_df = curves_df[~(curves_df == 0).any(axis=1)]
        
        self.ytrue=curves_df[Columns[0]]
        self.ypred=curves_df[Columns[1]]
        
        if save=='':
            plotter.lines(self,BBDDs=BBDDs,Columns=Columns,frequencies=[frequencies,frequencies], y_label=y_label, title=title, legend=legend, signs=[abs(signs[i]) for i in range(len(signs))], days_from_today=days_from_today, ndays=ndays, input_df=[curves_df] )
        else:
            plotter.lines(self,BBDDs=BBDDs,Columns=Columns,frequencies=[frequencies,frequencies], y_label=y_label, title=title, legend=legend, signs=[abs(signs[i]) for i in range(len(signs))], days_from_today=days_from_today, ndays=ndays, input_df=[curves_df], save=save )
        
        return {'forecast_error':self.forecast_error(),'MAPE':self.MAPE(),'RMSE':self.RMSE(),'bias':self.bias(),'mae':self.mae()}
        
        
       
    def forecast_error(self):
        return self.ytrue - self.ypred
    
    def MAPE(self):
        try:
            y_true, y_pred = np.array(self.ytrue), np.array(self.ypred)
            return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        except:
            pass
    
    def RMSE(self):
        try:
            return sqrt(mean_squared_error(self.ytrue, self.ypred))
        except:
            pass
        
    def bias(self):
        try:
            return np.mean(self.ytrue - self.ypred)
        except:
            pass        
        
    def mae(self):
        try:
            return mean_absolute_error(self.ytrue, self.ypred)
        except:
            pass
        
if __name__ == '__main__':   
    
    plots=plotter()
    #consum vs producció
    #plots.lines(BBDDs=['grid_BBDD'],Columns=['P_PV [kW]','P_load [kW]'],frequencies=[10,30],y_label='power kW',title='Production vs consumption', legend=['Production','Consumption'], signs=[1,-1],days_from_today=-7,ndays=5,save='consum_vs_producció_setmana') #,save='consum vs producció'
    
    #producció vs producció prevista
    #plots.lines(BBDDs=['grid_BBDD','PV_forecast_BBDD','PV_corr_forecast_BBDD'],Columns=['P_PV [kW]','p_mp','corr_p_mp'],frequencies=[30,30,30],y_label='power kW',title='Real pv production vs forecasted vs corrected forecast',legend=['Real production','Forecasted production','corrected forecast'], signs=[1,1,1],days_from_today=-16,ndays=16)
    
    #consum vs consum previst
    #plots.lines(BBDDs=['grid_BBDD','loads_forecast'],Columns=['P_load [kW]','P_load'],frequencies=[1,1],y_label='power kW',title='Real consumption vs forecasted',legend=['Real consumption','Forecasted consumption'], signs=[-1,-1],days_from_today=-7,ndays=1,save='consumption vs forecasted')
    
    #consumption plots
    #plots.lines(BBDDs=['grid_BBDD'],Columns=['P_load [kW]'],frequencies=[30],y_label='power kW',title='Sunday consumption', legend=['Consumption'], signs=[-1],days_from_today=-7,ndays=7,save='consum setmana') #,save='consum vs producció'
    
    
    #car
    #plots.lines(BBDDs=['car_BBDD'],Columns=['battery temperature'],frequencies=[15],y_label='km',title='Car mileage', legend=['mileage'], signs=[1],days_from_today=-1,ndays=1,save='car mileage')
    
    #grid
    #plots.lines(BBDDs=['grid_BBDD','PV_corr_forecast_BBDD'],Columns=['DC voltage [V]','v_mp'],frequencies=[1,1],y_label='Voltage V',title='DC voltage comparison', legend=['Real DC voltage','Corrected modeled DC voltage'], signs=[1,1],days_from_today=-10,ndays=5,save='DC voltages')
    
    #net balance
    #plots.lines(BBDDs=['grid_BBDD'],Columns=['P_grid [kW]'],frequencies=[1],y_label='power kW',title='Grid net power',legend=['Grid power'], signs=[1],days_from_today=-7,ndays=2,save='Grid balance')
    
    # weather
    #plots.lines(BBDDs=['forecast_weather_BBDD','current_weather_BBDD'],Columns=['clouds all','clouds all'],frequencies=[1,1],y_label='speed m/s, cloudiness index pu',title='Wind speed and cloudiness',legend=['Wind speed','cloudiness index'], signs=[1, 1],days_from_today=-7,ndays=7)
    
    #REE
    #plots.lines(BBDDs=['REE_BBDD'],Columns=[0,1,13],frequencies=[60,60,60],y_label='speed m/s, cloudiness index pu',title='Wind speed and cloudiness',legend=['Wind speed','cloudiness index','A'], signs=[1, 1,1],days_from_today=-17,ndays=18,save='PREUS')
    
    
    
    sc=scoring()
    pv_scores=sc.some_scores(BBDDs=['grid_BBDD','PV_forecast_BBDD'],Columns=['P_PV [kW]','p_mp'],frequencies=15, signs=[1,1],days_from_today=-16,ndays=16,title='Production forecast scoring graph',save='Production forecast scoring graph')
    
    pv_corr_scores=sc.some_scores(BBDDs=['grid_BBDD','PV_corr_forecast_BBDD'],Columns=['P_PV [kW]','corr_p_mp'],frequencies=15, signs=[1,1],days_from_today=-16,ndays=16,title='Production corrected weather scoring graph',save='Production corrected weather scoring graph')
    
    load_scores=sc.some_scores(BBDDs=['grid_BBDD','loads_forecast'],Columns=['P_load [kW]','P_load'],frequencies=5, signs=[-1,-1],days_from_today=-16,ndays=16,y_label='Consumption kW',title='Consumption forecast scoring',save='Consumption forecast scoring')
    
    cloud_scores=sc.some_scores(BBDDs=['current_weather_BBDD','forecast_weather_BBDD'],Columns=['clouds all','clouds all'],frequencies=15, signs=[1,1],days_from_today=-16,ndays=16,y_label='Cloudiness index',title='Weather forecast cloudiness scoring',save='Cloudiness scoring')
    temperature_scores=sc.some_scores(BBDDs=['current_weather_BBDD','forecast_weather_BBDD'],Columns=['main temp','main temp'],frequencies=15, signs=[1,1],days_from_today=-16,ndays=16,y_label='Temperature K',title='Weather forecast temperature scoring',save='Temperature scoring')
    wind_speed_scores=sc.some_scores(BBDDs=['current_weather_BBDD','forecast_weather_BBDD'],Columns=['wind speed','wind speed'],frequencies=15, signs=[1,1],days_from_today=-16,ndays=16,y_label='Wind speed m/s',title='Weather forecast wind speed scoring',save='Wind speed scoring')
    
    