# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:53:11 2020

@author: adria.bove
"""
from data_caller import datacall #, datagive
from datetime import datetime
from inputimeout import inputimeout, TimeoutOccurred



#init

call=datacall()

something ='continue'
while something =='continue':
    
    
    print(datetime.now())
    print('inici call')
    call.caller()
    
    print('fin calls')
    
    try:
        something = inputimeout(prompt='If you want to stop the loop type something: ', timeout=10)
    except TimeoutOccurred:
        something = 'continue'
        
    if something!='continue':
        print('Stopping loop')
    else:
        print('vuelta')
