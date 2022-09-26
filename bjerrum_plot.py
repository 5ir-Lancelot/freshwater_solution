# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 20:39:42 2021

@author: watda

create a bjerrum plot for seawater

so that this time consuming operation does not have to be repeated everytime
"""

# import the package
import PyCO2SYS as pyco2


#package to work with html documents
#import dash_html_components as html



import pandas as pd


#for the line plot take range of pH
pH_range=np.linspace(0,14,1000)

#fractions
lines=pd.DataFrame(data=np.zeros([pH_range.size,4]),columns=['pH','CO2_frac','HCO3_frac','CO3_frac'])
lines['pH']=pH_range

for item in lines.index:
    res=pyco2.sys(par1=pH_range[item],par2=400,par1_type=3,par2_type=4)
    
    lines.loc[item,'CO2_frac']=res['CO2']/res['dic']
    lines.loc[item,'CO3_frac']=res['CO3']/res['dic']
    lines.loc[item,'HCO3_frac']=res['HCO3']/res['dic']


#save it as csv
    
lines.to_csv('bjerrum_plot.csv', index=False, encoding='utf-8')
