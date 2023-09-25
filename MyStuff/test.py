import xml.etree.ElementTree as ET
import pandas as pd
from xml.dom.minidom import parse, parseString, Node

file = "Shops\RetailProductPrices.xml"
doc = parse(file)
print (doc.nodeName)
print(doc.firstChild.tagName)

nodes = doc.getElementsByTagName('Node')
dataframes_by_type = {}

# Define file paths
gvehicleFilePath = r'Data\Libs\Foundry\Records\Entities\GroundVehicles'
shipFilePath = r'Data\Libs\Foundry\Records\Entities\Spaceships'
partFilePath = r'Data\Libs\Foundry\Records\Entities\SCItem\Ships'

for node in nodes:
    node_id = node.getAttribute('ID')
    node_name = node.getAttribute('Name')
    node_price = node.getAttribute('BasePrice')
    node_file = node.getAttribute('Filename')

    if "Template" in node_name:
        continue
    else:
        # Extract the relevant part of the filepath to name the DataFrame
        df_name = None
        if gvehicleFilePath in node_file:
            df_name = 'GroundVehicles'
        elif shipFilePath in node_file:
            df_name = 'Spaceships'
        else:
            parts = node_file.split('\\SCItem\\Ships\\')
            if len(parts) == 2:
                part_type = parts[1].split('\\')[0]
                df_name = part_type
            else:
                part_type = 'Unknown'
        
        if df_name:
            # Check if DataFrame exists for this filepath, if not, create one
            if df_name not in dataframes_by_type:
                dataframes_by_type[df_name] = pd.DataFrame(columns=['ID', 'Name', 'BasePrice', 'Filename'])  # Adjust column names accordingly
        
            # Add data to the respective DataFrame
            new_df = pd.DataFrame({
                'ID': [node_id],
                'Name': [node_name],
                'BasePrice': [node_price],
                'Filename': [node_file]
            })
            
            # Concatenate the new DataFrame with the existing DataFrame for the specified df_name
            dataframes_by_type[df_name] = pd.concat([dataframes_by_type[df_name], new_df], ignore_index=True)

# Print the DataFrames
for df_name, df in dataframes_by_type.items():
    print(f"DataFrame for {df_name}:")
    print(df)