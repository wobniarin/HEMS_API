# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:35:42 2020

@author: adria.bove
"""

from HEMS_API.BBDD import BBDD
from HEMS_API import analytics

# create the objects
forecast_weather_BBDD=BBDD('forecast_weather_BBDD')
current_weather_BBDD=BBDD('current_weather_BBDD')
REE_BBDD=BBDD('REE_BBDD')
grid_BBDD=BBDD('grid_BBDD')
car_BBDD=BBDD('car_BBDD')

loads_forecast_BBDD=BBDD('loads_forecast')
PV_corr_forecast_BBDD=BBDD('PV_corr_forecast_BBDD')
PV_forecast_BBDD=BBDD('PV_forecast_BBDD')


#import the BBDDs
fore_w_df=forecast_weather_BBDD.import_BBDD()
curr_w_df=current_weather_BBDD.import_BBDD()
REE_df=REE_BBDD.import_BBDD()
grid_df=grid_BBDD.import_BBDD()
car_df=car_BBDD.import_BBDD()

fore_l_df=loads_forecast_BBDD.import_BBDD()
corr_PV_df=PV_corr_forecast_BBDD.import_BBDD()
fore_PV_df=PV_forecast_BBDD.import_BBDD()




