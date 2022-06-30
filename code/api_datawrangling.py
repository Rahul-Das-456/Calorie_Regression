import requests
import pprint as pp
import pandas as pd
pd.set_option('max_rows', 99999)
pd.set_option('max_colwidth', 400)

url = "https://api.edamam.com/api/nutrition-data?app_id=aba82731&app_key=793acdcce19384d28aa31dbd04ae2e42&nutrition-type=logging&ingr=Spicy%20Garlic-Chili%20Oil%20and%20Pasta"

response = requests.get(url)

data = response.json()
# Create DataFrame from data dictionary
# - set_index(0) makes the keys (columns) the index values
# - .T takes the transpose and makes the index the columns
# .reset_index(drop=True) resets index to 0 (1 row DataFrame) and drops old index
df = pd.DataFrame(data.items()).set_index(0).T.reset_index(drop=True)

# Select first 3 columns to keep as is
df = df[['calories', 'cautions', 'dietLabels']]

# For loop logic to create all other columns
# Since not all keys from totalNutrients are wanted, they must be selected in col_list
col_list = ['CA', 'CHOLE', 'FAT', 'FE', 'FIBTG', 'K', 'MG', 'NA', 'PROCNT', 'SUGAR', 'VITC']
value_list = []

# For each key and value (dictionary) in data['totalNutrients']
for key, value in data['totalNutrients'].items():
    # If key is in col_list
    if key in col_list:
        # Add value to value_list
        value_list.append(value['quantity'])
        
# Create dictionary of columns and values using zip()
clean_data_dict = dict(zip(col_list, value_list))

# Concatenate df with new DataFrame on the same index. axis=1 to concatenate on columns
df = pd.concat([df, pd.DataFrame(clean_data_dict, index=[0])], axis=1)

print(df)

try:
    main_df = pd.read_csv('data.csv')
    main_df = pd.concat([main_df, df])
    main_df.reset_index(drop=True, inplace=True)
    print(main_df)
    main_df.to_csv('data.csv', index=False)
except FileNotFoundError:
    df.to_csv('data.csv', index=False)

# OPTIONAL
# To change the column names at the end you can repeat the zip process
new_col_list = ["calories", "cautions", "diet_labels", "calcium", "cholesterol", "fat", "iron", "dietary_fiber", "potasssium", "magnesium", "sodium", "protein", "sugar", "vitamin_c"]

col_dict = dict(zip(col_list, new_col_list))

# .rename() uses a dict to map old column names to new column names
df.rename(columns=col_dict)

print(df)


lst = [
       
     
     
   
     
       "Spicy Garlic-Chili Oil and Pasta",      
       "Caprese Chicken Pesto Pasta", "Multi-Grain Pasta and Lamb, Butternut Squash, and Kasseri Cheese", "Bowtie Pasta and Asparagus"       
       
       ]

print(len(lst))