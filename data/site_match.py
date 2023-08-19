import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

"""##Vectorize the merged file and match"""

# Load your dataset
site_info = pd.read_csv('/Users/susu/Desktop/GovHack/merged_site_info_file.csv')
site_id= site_info['HOITEMID']
site_name= site_info['ITEMNAME']
des_info = site_info['description_json']
sig_info=site_info['significance_json']

# Vectorize the data
vectorizer = TfidfVectorizer(min_df=1, analyzer='word', ngram_range=(1, 2))
site_tfidf = vectorizer.fit_transform(site_name)
print('vectorize finished')

# Input a site name
site_name_input = input('Enter a site name: ')

#Initialize the Nearest Neighbors model
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

# print(' ')
# print(f"Matched Site id: {matched_site_id}")
# print(' ')
# print(f"Matched Site Name: {matched_site_name}")
# print(' ')
# print(f"Matched Description: {matched_des_info}")
# print(' ')
# print(f"Matched Significance: {matched_sig_info}")