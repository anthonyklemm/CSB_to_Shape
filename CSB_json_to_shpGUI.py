# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:57:44 2020

This script automates the conversion geojson files to shapefile, specifically for crowdsourced bathymetry (CSB) files (in JSON format)
downloaded from the Internation Hydrographic Organization's (IHO) Data Centre for Digital Bathymetry 
Crowdsourced Bathymetry Database. 

CSB data can be downloaded from this website: https://maps.ngdc.noaa.gov/viewers/iho_dcdb/
The output is a shapefile.


@author: Anthony Klemm
anthony.r.klemm@noaa.gov
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

import PySimpleGUI as sg
import sys

if len(sys.argv) == 1:
    directory = sg.popup_get_folder('Choose folder with CSB json files')
else:
    directory = sys.argv[1]

if not directory:
    sg.popup("Cancel", "No filename supplied")
    raise SystemExit("Cancelling: no filename supplied")
else:
    sg.popup('The filename you chose was', directory + '\n\nShapefiles will be saved in this same folder')

#directory = r'G:\csb\json\vero beach'
files = []

os.chdir(directory)
path = os.path.join(directory, 'shapefiles')

try:
    os.mkdir(path)
except Exception:
            pass
path = path.replace('\\', '/')
print(path)
os.chdir(path)
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
            csb.to_file(title +'.shp', driver='ESRI Shapefile')
        except Exception:
            pass
  
if __name__=="__main__":
    getFiles()
    ConvertJson()
