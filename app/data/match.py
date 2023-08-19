from google.colab import drive
import geopandas
import pandas as pd
from bs4 import BeautifulSoup
import json
import requests
import os
import time
from data_utils import des_parse_html,sig_parse_html

centroids_root_path='' #? not sure how to input the root
g = geopandas.read_file(centroids_root_path)
g['HOITEMID'] = g['HOITEMID'].astype(int)
print(g)
#g.to_csv('/content/GovHack/centroids.csv', index=False)

centroids_file_path = '/GovHack/centroids.csv'
html_folder_path = ' '  #?

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

output_csv_file_path = '/GovHack/merged_site_info_file.csv'
df.to_csv(output_csv_file_path, index=False, encoding='utf-8')

#print('Extraction and merging completed.')

"""##This part is only for checking the parsed file"""

# Load your dataset (replace 'your_dataset.csv' with your actual dataset file)
site_info = pd.read_csv('/GovHack/merged_site_info_file.csv')
# print(site_info.head(50))
# print('========================================')
for i in range(0,20):
  print(site_info.loc[i,'HOITEMID'])
  print(site_info.loc[i,'ITEMNAME'])
  print(site_info.loc[i,'description_json'])
  print(site_info.loc[i,'significance_json'])
  print('========================================')

"""##Vectorize the merged file and match"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import time

# Load your dataset
site_info = pd.read_csv('/GovHack/merged_site_info_file.csv')
site_id= site_info['HOITEMID']
site_name= site_info['ITEMNAME']
des_info = site_info['description_json']
sig_info=site_info['significance_json']

# Vectorize the data
vectorizer = TfidfVectorizer(min_df=1, analyzer='word', ngram_range=(1, 2))
site_tfidf = vectorizer.fit_transform(site_name)

# Input a site name
site_name_input = input('Enter a site name: ')

# Initialize the Nearest Neighbors model
nbrs = NearestNeighbors(n_neighbors=10, n_jobs=-1).fit(site_tfidf)

# Function to retrieve matched site information using indices
def get_matched_info(query_name, vectorizer, nbrs):
    query_tfidf = vectorizer.transform([query_name])
    distances, indices = nbrs.kneighbors(query_tfidf)
    matched_indices = indices[0]

    matched_site_ids= [site_id[i] for i in matched_indices]
    matched_site_names = [site_name[i] for i in matched_indices]
    matched_descriptions = [des_info[i] for i in matched_indices]
    matched_significances = [sig_info[i] for i in matched_indices]

    return matched_site_ids,matched_site_names, matched_descriptions, matched_significances

matched_site_id,matched_site_name, matched_des_info, matched_sig_info = get_matched_info(
    site_name_input, vectorizer, nbrs)

print(' ')
print(f"Matched Site id: {matched_site_id}")
print(' ')
print(f"Matched Site Name: {matched_site_name}")
print(' ')
print(f"Matched Description: {matched_des_info}")
print(' ')
print(f"Matched Significance: {matched_sig_info}")




