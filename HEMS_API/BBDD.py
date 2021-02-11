# -*- coding: utf-8 -*-
"""
Created on Fri May  8 23:34:49 2020

@author: adria.bove
"""
"""
import pickle


todo = {'header' :['write blog post', 'reply to email', 'read in a book']}

for i in range(4):
    pickle_file = open('todo.pickle', 'wb')
    pickle.dump(todo, pickle_file)
    del todo
    
     
    pickle_file = open('todo.pickle','rb')
    todos = pickle.load(pickle_file)
    todo=todos+{str(i) :['asdf','qerwt']}
    print(todo)
    
"""

import pandas as pd
from datetime import datetime, timedelta

class BBDD:
    def __init__(self,nom_BBDD):
        """
        

        Parameters
        ----------
        nom_BBDD : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.nom_BBDD=nom_BBDD+'.p'

    
    def store_data(self,objecte):
        
        if str(type(objecte))=="<class 'pandas.core.frame.DataFrame'>":
            if self.check_BBDD_exists()==0:
                self.BBDD =objecte
                self.save_to_pickle()
            else:
                self.BBDD=self.import_BBDD()
                self.BBDD=self.BBDD.append(objecte)
                
                self.BBDD = self.BBDD.drop_duplicates(subset='dt', keep='last')
                self.BBDD = self.BBDD.sort_values(by=['dt'])
                self.BBDD = self.BBDD.reset_index(drop=True)
                
                self.save_to_pickle()
        else:
        
            if self.check_BBDD_exists()==0:
                columns=list(objecte[0].keys())
                empty_lists_list=[[] for i in range(len(objecte[0]))]
                initiate_bbdd=dict(zip(columns, empty_lists_list))
                self.BBDD = pd.DataFrame(initiate_bbdd)
                
                self.fill_BBDD(objecte)
                self.save_to_pickle()
                
            else:
                self.BBDD=self.import_BBDD()
                self.fill_BBDD(objecte)
                self.save_to_pickle()
        


    def fill_BBDD(self, objecte):   
        a=len(self.BBDD.index)
        check=self.check_keys_dict_BBDD(objecte)
        if check!=True:
            for i in range(len(check)):
                empty_lists_list=[[] for h in range(a)]
                self.BBDD[check[i]]=empty_lists_list
            
            
        for i in range(len(objecte)):
            empty_lists_list=[[] for h in range(len(self.BBDD.keys()))]
            self.BBDD.loc[a+i] = empty_lists_list
            
            b=[b for b in objecte[i]]
            for n in b:
                self.BBDD[n][a+i]=objecte[i][n]
        
        self.BBDD = self.BBDD.drop_duplicates(subset='dt', keep='last')
        self.BBDD = self.BBDD.sort_values(by=['dt'])
        self.BBDD = self.BBDD.reset_index(drop=True)
        
        
    def check_BBDD_exists(self):
        try:
            pd.read_pickle(self.nom_BBDD)
            return 1
        except:
            return 0
        
    def import_BBDD(self):
        return pd.read_pickle(self.nom_BBDD)

    def check_keys_dict_BBDD(self,objecte):
        new_columns=[]
        for i in range(len(objecte)):
            list1=list(objecte[i].keys())
            list2=list(self.BBDD.keys())
            new_columns=new_columns+list(set(list1) - set(list2))
        new_columns = list(dict.fromkeys(new_columns))
        
        if new_columns==[]:
            return True
        else:
            return new_columns

    def save_to_pickle(self):
        self.BBDD.to_pickle(self.nom_BBDD)

    def _print_(self):
        self.BBDD=self.import_BBDD()
        print (self.BBDD)
        
    
    def extract(self,days_from_today:int=0, ndays:int=1):
        df=self.import_BBDD()
        today=datetime.strptime(datetime.today().__str__()[0:10], '%Y-%m-%d')
        
        df.dt = df.dt.apply(lambda d: d.replace(tzinfo=None))
        new_df=df[(df.dt >= today+timedelta(days=days_from_today)) & (df.dt < (today+timedelta(days=days_from_today+ndays)))]
        return new_df
        
        
        #new_df = df[df.dt >= init_time | df.dt <=init_time+duration]
        #return new_df
    
    def extract_pers(self,column_name,coincident_value):
        df=self.import_BBDD()

        new_df=df[(df[column_name] == coincident_value)]
        return new_df
    
    def extract_weekday(self,weekday):
        df=self.import_BBDD()
        df.index=df.dt
        df.index.names = ['Date']
        new_df=df[(df.index.weekday == weekday)]
        return new_df

    def last_entry_time(self):
        df=self.import_BBDD()
        last_time=max(df['dt'])
        return last_time




if __name__=='__main__':

    """
    my_df = pd.DataFrame()
    
    names = ['Bob', 'Sam', 'Jo', 'Bill']
    
    favourite_sports = [['Tennis', 'Motorsports'],
                       ['Football', 'Rugby', 'Hockey'],
                       ['Table tennis', 'Swimming', 'Athletics'],
                       ['Eating cheese']]
    
    my_df['name'] = names
    my_df['favourite_sport'] = favourite_sports
    
    print(my_df)
    
    
    # Save DataFrame to pickle object
    my_df.to_pickle('test_df.p')
    
    del my_df
    
    
    """
    # Load DataFrame with pickle object
    
    weather_BBDD=BBDD('REE_BBDD')
    weather_BBDD._print_()
    #weather_BBDD.store_data(forecast)
    


