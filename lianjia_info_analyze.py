# coding: utf-8
import pandas as pd
import csv 


df=pd.read_csv('data/lj.csv',encoding = "gbk",header=None,names=['district','district2','apm_section','apm_type','apm_size','story','price','url'])
df["apm_size_numeric"]=df.apm_size.str[:-1]
df["apm_size_numeric"]
pd.