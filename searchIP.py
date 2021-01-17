
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:34:59 2020

@author: adria.bove
"""

"""
We want to run a function asychronously and run a
callback function with multiple parameters when it
returns!
In this example, we are pretending we're analyzing
the names and ages of some people. We want to print
out:
jack 0
jill 1
james 2
"""

import time
from multiprocessing.dummy import Pool
import requests
import ipaddress
from functools import partial


class searchIPfronius():

    def __init__(self):
        pass
    
    def async_function(self,ip_inicial):
        """
        Function we want to run asynchronously and in parallel,
        usually one with heavy input/output, though using a
        dummy function here.
        """
        url='http://'+str(ip_inicial)+'/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'
        response=requests.get(url,timeout=2)    
        #time.sleep(1)
        response=response.json()
        
        return response['Body']['Data']['DAY_ENERGY']['Unit']
        
    def callback_function(self,status, ip_inicial):
        """
        Function we want to run with the result of the async
        function. The async function returns one parameter, but
        this function takes two parameters. We have to figure
        out how to pass the age parameter from the async function
        to this function..
        """
        if status=='Wh':
            #print(status, ip_inicial)
            self.ip_inversor=str(ip_inicial)



    def buscador(self):
        nIP_search=400
        pool = Pool(processes=nIP_search)
        #status=[]
        ip_inicial=ipaddress.ip_address('192.168.1.0')
        
        for ip in range(nIP_search):
        
            """
            Partial is a technique for creating a function that
            just calls another function but with one or more of
            the parameters "frozen". In this way, we can capture
            the 'ip_inicial' paramter in each iteration of the loop and
            pass it along with the return value of the async
            function.
            """
            ip_inicial=ip_inicial+1
            new_callback_function = partial(self.callback_function, ip_inicial=ip_inicial)
            pool.apply_async(
                self.async_function,
                args=[ip_inicial],
                callback=new_callback_function,
                error_callback=new_callback_function
            )
        
        pool.close()
        pool.join()


if '__main__'==__name__:
    
    start_time = time.time()
    
    sIP=searchIPfronius()
    sIP.buscador()
    print(sIP.ip_inversor)
    
    print("--- %s seconds ---" % (time.time() - start_time))
