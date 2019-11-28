 #!/usr/bin/env python3
 # -*- coding: utf-8 -*-
"""
 Created on Wed Oct  2 11:27:05 2019
 
 @author: sdandavathi
 @author_2:Karthick
"""
import os
import pandas as pd
import re
import datetime
import time
import json
import numpy as np

from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults,GetUpdatedPropertyDetails

# TODO  :  change this per your pc location
cwd = r'C:\Users\karth\OneDrive\Desktop\Project_research\Final_Project_files\Address_files' 


with open(cwd + '\\split_by_date.json','r') as f: #download this file from google drive to your pc
    Data = json.load(f)
today = datetime.datetime.today().date()
today_data = Data[str(today)]
#myData is a list of Dicts        
    
Final_data = pd.DataFrame()
count= 0
api_count = 0
###
### Change below to use your own API Keys 
api_keys = ['XXXXXX','YYYYYY','XZZZZZZ]
##next_day = datetime.datetime.combine(next_day,datetime.datetime.min.time()) + datetime.timedelta(hours=2)
new = []
for each_address in today_data:   
    street_address = each_address['NUMBER'] + ' ' + each_address['STREET']
    zipcode = each_address['POSTCODE']
    zillow_data = ZillowWrapper(api_keys[api_count])
    try:
        count = count + 1 #Being conservative here , i want to count even if the address failed
        deep_search_response = zillow_data.get_deep_search_results(street_address, zipcode)
        result = GetDeepSearchResults(deep_search_response)
    except:
        continue
    mydict = {}
    mydict['Address'] = street_address
    mydict['ZIP'] = zipcode
    mydict["zillow_id"]=result.zillow_id
    mydict["home_type"]=result.home_type
    mydict["year_built"]=result.year_built
    mydict["property_size"]=result.property_size
    mydict["home_size"]=result.home_size
    mydict["bathrooms"]=result.bathrooms
    mydict["bedrooms"]=result.bedrooms
    mydict["zestimate_amount"]=result.zestimate_amount
    mydict["zestimate_percentile"]=result.zestimate_percentile
    mydict["tax_year"]=result.tax_year
    mydict["tax_value"]=result.tax_value
    mydict["latitude"]=result.latitude
    mydict["longitude"]=result.longitude
    new.append(mydict)
    print(count)
    if count >= 990:
        time.sleep(60)
        count=0
        api_count = api_count + 1

print("The length of the today's data is ", len(new))               
pd.DataFrame(new).to_pickle(cwd + '\\Output_zillow_data\\' + str(datetime.datetime.today().date())) #create a folder called Output_Zillow_data in your parent directory                
                
        

