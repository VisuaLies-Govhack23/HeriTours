import pandas as pd
import json

df = pd.read_csv('/Users/susu/Desktop/GovHack/site_info_file.csv')

result = []
for index, row in df.iterrows():
    data = {
        "id": int(row['HOITEMID']),
        "name": row['ITEMNAME'],
        "address": row['ADDRESS'],
        "lga": row['LGA'],
        "descprition_data": row['description_json'],
        "significance_data": row['significance_json']
    }
    result.append(data)

print(result[:5])

# save results
with open('/Users/susu/Desktop/GovHack/output.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)
