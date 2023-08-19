#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import numpy as np
import os


data_folder = "data/2021_PEP_all_for_NSW_short-header/2021 Census PEP All Geographies for NSW/LGA/NSW"

lga = gpd.read_file(
    "data/LGA_2021_AUST_GDA2020_SHP/LGA_2021_AUST_GDA2020.shp"
).drop("geometry", axis=1)

lga['LGA_CODE_2021'] = 'LGA'+lga['LGA_CODE21'].astype(str)

# Indigenous status data
is_df = pd.read_csv(os.path.join(data_folder, "2021Census_P07_NSW_LGA.csv"))

# Country of birth data
country_of_birth_df = pd.read_csv(
    os.path.join(data_folder, "2021Census_P09_NSW_LGA.csv")
)


column_dict = {
    "indigenous_status": [
        is_df,
        [
            "Tot_Indig_P",
            "Tot_Non_Indig_P",
            "Tot_Indig_status_ns_P",
        ],
    ],
    "country_of_birth": [
        country_of_birth_df,
        [x for x in country_of_birth_df if ("_P" in x) and ("Tot_P" not in x)],
    ],
}

total_population = is_df[["LGA_CODE_2021","Tot_Tot_P"]].rename(columns = {'Tot_Tot_P': 'Total population'})

expanded_col_dict = {}

# Concordance table manually created from the Census Metadata file (Metadata_2021_PEP_DataPack_R1_R2.xlsx)
table_conc = pd.read_csv('working/table_name_concordance.csv')

data_list = []

for category in sorted(column_dict.keys())[:1]:
    
    
    print(category)
    df_category = column_dict[category][0]
    
    df_columns = column_dict[category][1]
    
    df_category_group = df_category.groupby(['LGA_CODE_2021'])[df_columns].sum().reset_index()
    
    df_category_group['Total_' + category] = df_category_group[df_columns].sum(axis = 1)

    for col in df_columns:
        df_category_group[col + '_percentage'] = df_category_group[col] / df_category_group['Total_' + category]

    df_category_group_subset = df_category_group[['LGA_CODE_2021'] + [x for x in list(df_category_group) if 'percentage' in x]]

    expanded_name_list = table_conc[table_conc.Short.isin(column_dict[category][1])]

    if category == 'ancestry':
        expanded_name_list['updated'] = expanded_name_list['Long'].apply(lambda x: x.replace('Total_Responses','').replace('_',' '))
        
    elif category in ['country_of_birth' ,'indigenous_status']:
        expanded_name_list['updated'] = expanded_name_list['Long'].apply(lambda x: x.replace('Persons','').replace('_',' '))

    expanded_name_list['Short_updated'] = expanded_name_list['Short'] + '_percentage'

    expanded_name_dict = dict(zip(expanded_name_list.Short_updated, expanded_name_list.updated))

    expanded_name_dict['LGA_CODE_2021'] = 'LGA_CODE_2021'
    
    df_category_group_subset.columns = [expanded_name_dict[x] for x in df_category_group_subset.columns]
    df_category_group_subset = df_category_group_subset.merge(lga[['LGA_CODE_2021','LGA_NAME21']], on = 'LGA_CODE_2021', how = 'left')

    df_category_group_subset_melt = pd.melt(df_category_group_subset, id_vars = ['LGA_CODE_2021','LGA_NAME21'], value_vars = [x for x in df_category_group_subset if x not in ['SAL_CODE_2021','SAL_NAME21']], var_name = category, value_name = 'percentage')

    # df_category_group_subset_melt_top5 = df_category_group_subset_melt.sort_values('percentage',ascending = False).groupby(['LGA_CODE_2021','LGA_NAME21']).head(5).reset_index()

    df_category_group_subset_melt.to_csv('working/{}.csv'.format(category), index=False)
# 
