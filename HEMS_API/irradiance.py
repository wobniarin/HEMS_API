"""
GHI to POA Transposition
=========================

Example of generating clearsky GHI and POA irradiance.
"""

# 
# This example shows how to use the
# :py:meth:`pvlib.location.Location.get_clearsky` method to generate clearsky
# GHI data as well as how to use the
# :py:meth:`pvlib.irradiance.get_total_irradiance` function to transpose
# GHI data to Plane of Array (POA) irradiance.

from pvlib import location, irradiance
import pandas as pd
from matplotlib import pyplot as plt
from credentials import tilt,azimuth,latitud,longitud
from datetime import datetime, timedelta
from HEMS_API.BBDD import BBDD

class irradiation:
    def __init__(self,tilt_inp: int=None, azimuth_inp: int=None):
        # For this example, we will be using Golden, Colorado
        
        self.tz = 'Europe/Madrid'
        lat, lon = latitud, longitud
        self.tilt=tilt_inp
        self.surface_azimuth=azimuth_inp
        
        if tilt_inp==None:
            self.tilt=tilt
            self.surface_azimuth=azimuth
        
        # Create location object to store lat, lon, timezone
        self.site = location.Location(lat, lon, tz=self.tz)


        # Calculate clear-sky GHI and transpose to plane of array
        # Define a function so that we can re-use the sequence of operations with
        # different locations
        
    def get_net_irradiance(self, days_from_today: int=0, freq: int=15 , ndays: int=1):
        initial_date=(datetime.now()+timedelta(days=days_from_today)).strftime('%m-%d-%Y')
        site_location=self.site
        # Creates one day's worth of 10 min intervals
        times = pd.date_range(initial_date, freq=str(freq)+'min', periods=60/freq*24*ndays,
                              tz=site_location.tz)
        # Generate clearsky data using the Ineichen model, which is the default
        # The get_clearsky method returns a dataframe with values for GHI, DNI,
        # and DHI
        clearsky = site_location.get_clearsky(times)
        # Get solar azimuth and zenith to pass to the transposition function
        solar_position = site_location.get_solarposition(times=times)
        # Use the get_total_irradiance function to transpose the GHI to POA
        POA_irradiance = irradiance.get_total_irradiance(
            surface_tilt=self.tilt,
            surface_azimuth=self.surface_azimuth,
            dni=clearsky['dni'],
            ghi=clearsky['ghi'],
            dhi=clearsky['dhi'],
            solar_zenith=solar_position['apparent_zenith'],
            solar_azimuth=solar_position['azimuth'])
        # Return DataFrame with only GHI and POA. POA is the irradiance for the specified tilt and azimuth
        return pd.DataFrame({'GHI': clearsky['ghi'],
                             'POA': POA_irradiance['poa_global']})


    def get_params_PV_forecast_prod(self,BBDDs,freq,days_from_today:int=0,ndays: int=5):
        forecast_weather_BBDD=BBDD(BBDDs)
        weather_df=forecast_weather_BBDD.extract(days_from_today,ndays)
        weather_df=weather_df.reset_index(drop=True)
        #times = pd.date_range(weather_df['dt'][0], freq=str(freq)+'min', periods=60/freq*24*ndays,tz=irr.site.tz)
        
        irradiance=self.get_net_irradiance(days_from_today,freq,ndays)
        POA_irradiance=irradiance['POA']
        
        weather_df['dt'] = pd.to_datetime(weather_df['dt'])
        weather_df.index = weather_df['dt']
        weather_df=weather_df.tz_localize(self.tz)
        del weather_df['dt']
        #plt.plot(weather_df['main temp'])
        for col in weather_df:
            weather_df[col] = pd.to_numeric(weather_df[col], errors='coerce')
        weather_df=weather_df.resample(str(freq)+'T').pad()
        #weather_df = weather_df.interpolate()
        #plt.plot(weather_df['main temp'])
        df =weather_df.join(POA_irradiance, lsuffix='_caller', rsuffix='_other')
        df['eff_irrad']=(1-df['clouds all']/100)*df['POA']
        
        return df

    def _plot(self,objecte):

        # Convert Dataframe Indexes to Hour:Minute format to make plotting easier
        objecte.index = objecte.index.strftime("%H:%M")

        
        # Plot GHI vs. POA for winter and summer
        fig, (ax1) = plt.subplots(1, 1, sharey=True)
        objecte['GHI'].plot(ax=ax1, label='GHI')
        objecte['POA'].plot(ax=ax1, label='POA')

        ax1.set_xlabel('Time of day (Today and tomorrow)')

        ax1.set_ylabel('Irradiance ($W/m^2$)')
        ax1.legend()

        plt.show()


if __name__=='__main__':
    # Get irradiance data for summer and winter solstice, assuming 25 degree tilt
    # and a south facing array
    irr=irradiation(tilt_inp=0, azimuth_inp=180)
    today = irr.get_net_irradiance()
    days_from_today=(datetime.now()-datetime(2020,1,1))
    today_tomorrow = irr.get_net_irradiance(days_from_today=days_from_today.days,freq=60,ndays=365)
    irr._plot(today_tomorrow)
    #df=irr.get_params_PV_forecast_prod('current_weather_BBDD',15,-5)
    
    
    #plt.plot(df['eff_irrad'])
    #plt.plot(df['POA'])
    #irr._plot(today_tomorrow)
    # 
    # Note that in Summer, there is not much gain when comparing POA irradiance to
    # GHI. In the winter, however, POA irradiance is significantly higher than
    # GHI. This is because, in winter, the sun is much lower in the sky, so a
    # tilted array will be at a more optimal angle compared to a flat array.
    # In summer, the sun gets much higher in the sky, and there is very little
    # gain for a tilted array compared to a flat array.
