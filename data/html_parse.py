import geopandas
import pandas as pd
from bs4 import BeautifulSoup
import json
import os
from data.data_utils import des_parse_html,sig_parse_html

centroids_root_path='/Users/susu/Desktop/GovHack/centroids/'
g = geopandas.read_file(centroids_root_path)
g['HOITEMID'] = g['HOITEMID'].astype(int)
g.to_csv('/Users/susu/Desktop/GovHack/centroids.csv', index=False)

centroids_file_path = '/Users/susu/Desktop/GovHack/centroids.csv'
html_folder_path = '/Users/susu/Desktop/GovHack/pages/'

df = pd.read_csv(centroids_file_path)
description_json=[]
significance_json=[]

for index, row in df.iterrows():
    hoitemid = row['HOITEMID']
    description_html_path = os.path.join(html_folder_path, f'{hoitemid}.description.html')
    significance_html_path = os.path.join(html_folder_path, f'{hoitemid}.significance.html')
    if os.path.exists(description_html_path) and os.path.exists(significance_html_path):
        # read HTML contents
        with open(description_html_path, 'r', encoding='utf-8') as description_file, \
            open(significance_html_path, 'r', encoding='utf-8') as significance_file:
            description_content = description_file.read()
            significance_content = significance_file.read()

            # parse HTML
            if description_content is not None:
                des_json_data = des_parse_html(description_content)
                description_json.append(des_json_data)
            else:
                description_json.append('None')

            if significance_content is not None:
                sig_json_data = sig_parse_html(significance_content)
                significance_json.append(sig_json_data)
            else:
                significance_json.append('None')
    else:
        description_json.append('None')
        significance_json.append('None')

df['description_json']=description_json
df['significance_json']=significance_json

output_csv_file_path = '/Users/susu/Desktop/GovHack/site_info_file.csv'
df.to_csv(output_csv_file_path, index=False, encoding='utf-8')
print('finished sites info merge')
#print('Extraction and merging completed.')

# """##This part is only for checking the parsed file"""
#
# site_info = pd.read_csv('/Users/susu/Desktop/GovHack/merged_site_info_file.csv')
# # print('========================================')
# for i in range(0,20):
#   print(site_info.loc[i,'HOITEMID'])
#   print(site_info.loc[i,'ITEMNAME'])
#   print(site_info.loc[i,'description_json'])
#   print(site_info.loc[i,'significance_json'])
#   print('========================================')






