#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import geopandas as gpd

sal = gpd.read_file('SAL_2021_AUST_GDA2020_SHP/SAL_2021_AUST_GDA2020.shp')
sal.geometry = sal.geometry.to_crs('epsg:4326')

heritage_data_gdf = gpd.read_file('govhack/Heritage_HistoricHeritageSites/HistoricHeritageSites.shp')
heritage_data_gdf.geometry = heritage_data_gdf.geometry.to_crs('epsg:4326')

heritage_data_gdf['longitude'] = heritage_data_gdf.geometry.x
heritage_data_gdf['latitude'] = heritage_data_gdf.geometry.y

heritage_data_gdf['lat_long'] = heritage_data_gdf.apply(lambda df: [df.latitude, df.longitude], axis = 1)

heritage_suburbs = gpd.sjoin(heritage_data_gdf[['OBJECT_ID','ITEM_NAME','lat_long','geometry']],
                           sal[['SAL_CODE21','SAL_NAME21','geometry']])

# heritage_data_df = heritage_data_gdf.drop('geometry', axis = 1)

heritage_df = heritage_suburbs[['OBJECT_ID',
 'ITEM_NAME','SAL_NAME21','SAL_CODE21',
 'lat_long']]


heritage_df.to_csv('govhack/heritage_data_suburb.csv', index=False)
