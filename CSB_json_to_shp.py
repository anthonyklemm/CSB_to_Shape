# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:57:44 2020

This script automates the tide correction of crowdsourced bathymetry (CSB) files (in JSON format)
downloaded from the Internation Hydrographic Organization's (IHO) Data Centre for Digital Bathymetry 
Crowdsourced Bathymetry Database. 

The output is a shapefile.


@author: Anthony Klemm
"""


import geopandas as gpd
import numpy as np
import pandas as pd
import json
import requests
import fiona
import os
import glob
import ntpath
pd.set_option('display.max_columns', None)

directory = r'G:\csb\json\vero beach'
files = []

os.chdir(directory)
#fp_zones = r"E:\csb\tide zone polygons\tide_zone_polygons.shp"

def getFiles():
    for filepath in glob.iglob(directory + '/*.json', recursive=False):
        files.append(filepath)
        
def ConvertJson():
    nameList = []
    for filepath in files:
        head, filename = ntpath.split(filepath)
        title = filename[15:]
        nameList.append(title)
        print("Reading file: "+filename)
        csb = gpd.read_file(filepath)
        y=open(filepath)
        x=json.load(y)
        csb['name']= x['properties']['platform']['name']
          
            
        csb = csb.dropna()
        
                  
        csb = gpd.GeoDataFrame(csb, geometry='geometry', crs='EPSG:4326')
        #csb['time'] = csb['time'].dt.strftime("%Y%m%d %H:%M")
        #filter out depths less than 1.5m and greater than 1000m
        csb = csb[csb['depth'] > 1.5]
        csb = csb[csb['depth'] < 1000]
        print(csb)
        try:   
            csb.to_file('G:/csb/shapefiles/vero beach/csb_no_tide'+ title +'.shp', driver='ESRI Shapefile')
        except Exception:
            pass
   
if __name__=="__main__":
    getFiles()
    ConvertJson()
