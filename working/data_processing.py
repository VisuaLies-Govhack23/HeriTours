#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import numpy as np
import os

#%%

sal = gpd.read_file('SAL_2021_AUST_GDA2020_SHP/SAL_2021_AUST_GDA2020.shp')
sal.geometry = sal.geometry.to_crs('epsg:4326')


gdf = gpd.read_file('govhack/Heritage_HistoricHeritageSites/HistoricHeritageSites.shp')
gdf.geometry = gdf.geometry.to_crs('epsg:4326')
# df = gdf.drop('geometry',axis = 1)

heritage_items = gpd.sjoin(gdf[['OBJECT_ID','ITEM_NAME','ITEM_STATU','geometry']],
                           sal[['SAL_CODE21','SAL_NAME21','geometry']])

df_group = heritage_items.groupby(['SAL_NAME21','SAL_CODE21','ITEM_STATU']).ITEM_NAME.count().reset_index()

df_group.to_csv('govhack/heritage_data.csv', index=False)


#%%

sal['SAL_CODE_2021'] = 'SAL' + sal.SAL_CODE21.astype(str)


#%%

# Census
"""
- Population
- Indigenous status - I02 / P07
# - Ethnicity
- Country of birth - P09
- Ancestry - P08

Size: 382 wide by 664 high 

"""


# Indigenous status

is_folder = 'data/2021_census/2021_IP_all_for_NSW_short-header/2021 Census IP All Geographies for NSW/SAL/NSW'

is_df = pd.read_csv('data/2021_census/2021_IP_all_for_NSW_short-header/2021 Census IP All Geographies for NSW/SAL/NSW/2021Census_I02_NSW_SAL.csv')

is_data_col = [
 # 'Indigenous_Aboriginal_P',

 # 'Indigenous_Torres_Strait_Is_P',

 # 'Indig_Bth_Abor_Torr_Strt_Is_P',

  'Indigenous_TotP',

 'Non_Indig_P',

 'Indigenous_status_nsP',

 'Tot_P']

is_df_group = is_df.groupby(['SAL_CODE_2021'])[is_data_col].sum().reset_index()

is_df_group['total_calc'] = is_df_group[[x for x in is_data_col if x != 'Tot_P']].sum(axis = 1)

for x in [x for x in is_data_col if x != 'Tot_P']:
    is_df_group[x + '_proportion'] = is_df_group[x] / is_df_group['total_calc']
    
#%%

data_folder = 'data/2021_census/2021_PEP_all_for_NSW_short-header/2021 Census PEP All Geographies for NSW/SAL/NSW'





is_df = pd.read_csv(os.path.join(data_folder, '2021Census_P07_NSW_SAL.csv'))

ancestry_df = pd.read_csv(os.path.join(data_folder, '2021Census_P08_NSW_SAL.csv'))

country_of_birth_df = pd.read_csv(os.path.join(data_folder, '2021Census_P09_NSW_SAL.csv'))
    

column_dict = {'indigenous_status': [is_df, [ 'Tot_Indig_P',
 'Tot_Non_Indig_P',
 'Tot_Indig_status_ns_P',]],
               
               # 'ancestry': [ancestry_df,[x for x in ancestry_df if ('_Tot_R' in x) and ('Tot_P' not in x)]],
               
               'country_of_birth': [country_of_birth_df, [x for x in country_of_birth_df if ('_P' in x) and ('Tot_P' not in x)]]
               
               
               }


expanded_col_dict = {}

table_conc = pd.read_csv('data/table_concordance.csv',skiprows = 1)

data_list = []

for category in sorted(column_dict.keys()):
    
    
    print(category)
    df_category = column_dict[category][0]
    
    df_columns = column_dict[category][1]
    
    
    df_category_group = df_category.groupby(['SAL_CODE_2021'])[df_columns].sum().reset_index()
    
    df_category_group['Total_' + category] = df_category_group[df_columns].sum(axis = 1)

    for col in df_columns:
        df_category_group[col + '_percentage'] = df_category_group[col] / df_category_group['Total_' + category]

    df_category_group_subset = df_category_group[['SAL_CODE_2021'] + [x for x in list(df_category_group) if 'percentage' in x]]

    # data_list.append(df_category_group_subset)
    
    
    expanded_name_list = table_conc[table_conc.b.isin(column_dict[category][1])]

    if category == 'ancestry':
        expanded_name_list['updated'] = expanded_name_list['c'].apply(lambda x: x.replace('Total_Responses','').replace('_',' '))
        
        # expanded_name_list = [x.replace('Total_Responses','').replace('_',' ') for x in expanded_name_list['c'].tolist()]

    elif category in ['country_of_birth' ,'indigenous_status']:
        expanded_name_list['updated'] = expanded_name_list['c'].apply(lambda x: x.replace('Persons','').replace('_',' '))
        
        
        # expanded_name_list = [x.replace('Persons','').replace('_',' ') for x in expanded_name_list['c'].tolist()]

    # elif category == 'indigenous_status':
    #     expanded_name_list = [x.replace('Persons','').replace('_',' ') for x in expanded_name_list['c'].tolist()]

    expanded_name_list['b_updated'] = expanded_name_list['b'] + '_percentage'

    expanded_name_dict = dict(zip(expanded_name_list.b_updated, expanded_name_list.updated))

    expanded_name_dict['SAL_CODE_2021'] = 'SAL_CODE_2021'
    
    df_category_group_subset.columns = [expanded_name_dict[x] for x in df_category_group_subset.columns]

    df_category_group_subset = df_category_group_subset.merge(sal[['SAL_CODE_2021','SAL_NAME21']], on = 'SAL_CODE_2021', how = 'left')

    df_category_group_subset_melt = pd.melt(df_category_group_subset, id_vars = ['SAL_CODE_2021','SAL_NAME21'], value_vars = [x for x in df_category_group_subset if x not in ['SAL_CODE_2021','SAL_NAME21']], var_name = category, value_name = 'percentage')

    df_category_group_subset_melt_top5 = df_category_group_subset_melt.sort_values('percentage',ascending = False).groupby(['SAL_CODE_2021','SAL_NAME21']).head(5).reset_index()

    df_category_group_subset_melt_top5.to_csv('govhack/{}.csv'.format(category), index=False)

    # print(df_category_group_subset.isnull().sum())

    # expanded_col_dict[category] = expanded_name_list
    
    
    
    # print(expanded_col_dict[category].shape[0], len(df_columns))
    
    

# data_list_df = pd.concat([x.set_index('SAL_CODE_2021') for x in data_list], axis = 1, join = 'inner').reset_index()

    