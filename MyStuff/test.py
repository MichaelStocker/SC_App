import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse

# Parse ShopLayouts.xml to create a dictionary mapping IDs to ShopLayoutNode names
shop_layouts_file = "Shops\\ShopLayouts.xml"
shop_layouts_root = ET.parse(shop_layouts_file).getroot()
id_to_shop_name = {}
for shop_node in shop_layouts_root.findall('.//ShopLayoutNode'):
    shop_name = shop_node.get('Name')
    for item_node in shop_node.findall('.//ShopInventoryNode'):
       inventoryID = item_node.get('InventoryID')
        

    
    id_to_shop_name[inventoryID] = shop_name

# Parse RetailProductPrices.xml
retail_prices_file = "Shops\\RetailProductPrices.xml"
productDoc = parse(retail_prices_file)
nodes = productDoc.getElementsByTagName('Node')

# Define file paths
gvehicleFilePath = r'Data\Libs\Foundry\Records\Entities\GroundVehicles'
shipFilePath = r'Data\Libs\Foundry\Records\Entities\Spaceships'
partFilePath = r'Data\Libs\Foundry\Records\Entities\SCItem\Ships'

dataframes_by_type = {}

# Iterate through nodes
for node in nodes:
    node_id = node.getAttribute('ID')
    node_name = node.getAttribute('Name')
    node_price = node.getAttribute('BasePrice')
    node_file = node.getAttribute('Filename')

    if node_id in id_to_shop_name:
        # Use the parent ShopLayoutNode name as the store location
        store_location = id_to_shop_name[node_id]
    else:
        store_location = "Unknown"  # Default if not found

    if "Template" in node_name:
        continue
    if float(node_price) == 0.0:
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
                dataframes_by_type[df_name] = pd.DataFrame(columns=['StoreLocation', 'Name', 'BasePrice', 'Filename'])  # Adjust column names accordingly
        
            # Add data to the respective DataFrame
            new_df = pd.DataFrame({
                'StoreLocation': [store_location],
                'Name': [node_name],
                'BasePrice': [node_price],
                'Filename': [node_file]
            })
            
            # Concatenate the new DataFrame with the existing DataFrame for the specified df_name
            dataframes_by_type[df_name] = pd.concat([dataframes_by_type[df_name], new_df], ignore_index=True)
printDF = True
# Print the DataFrames
if printDF:
    for df_name, df in dataframes_by_type.items():
        print(f"DataFrame for {df_name}:")
        print(df)


#shopList.append(shop_name)


#print(shopList)