import pandas as pd
suburb_file_path = '/Users/susu/Desktop/GovHack/shr_centroids_lat_long.csv'  # file from David
merged_site_path='/Users/susu/Desktop/GovHack/site_info_file.csv'   # heritage description and significance info
heritage_info_path='/Users/susu/Desktop/GovHack/heritage_info_file.csv'    # output the merged files
suburb_df = pd.read_csv(suburb_file_path)
site_df=pd.read_csv(merged_site_path)
suburb_df['HOITEMID'] = suburb_df['HOITEMID'].astype(int)
suburb_df.to_csv(suburb_file_path, index=False)

heritage_info_df = pd.merge(site_df,suburb_df,left_on='HOITEMID',right_on='HOITEMID', how='inner')

# Save the merged DataFrame to a new CSV file
heritage_info_df.to_csv(heritage_info_path, index=False)