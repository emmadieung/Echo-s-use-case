#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt

# Load Mobility_Data
mobility_data_url = "https://drive.google.com/uc?id=1ihvBQM2z7_utXrUI8Dw4IPfsNVUuJC2c"
mobility_data = pd.read_csv(mobility_data_url)

# Load POI_Data
poi_data_url = "https://drive.google.com/uc?id=1DXYNtYxYMAZGucjhsTdL_cysHAeLvjLY"
poi_data = pd.read_csv(poi_data_url)

# Apply the coefficient to estimate actual visits
mobility_data['estimated_visits'] = mobility_data['nb_point'] * 13.13

mobility_data, poi_data


# In[2]:


# Checking basic information about Mobility Data
print("Mobility Data Info:")
mobility_data.info()

# Checking for missing values in Mobility Data
print("\nMissing Values in Mobility Data:")
print(mobility_data.isnull().sum())

# Checking basic statistics of numeric columns in Mobility Data
print("\nStatistics of Numeric Columns in Mobility Data:")
print(mobility_data.describe())


# In[3]:


# Checking basic information about POI Data
print("\nPOI Data Info:")
poi_data.info()

# Checking for missing values in POI Data
print("\nMissing Values in POI Data:")
print(poi_data.isnull().sum())

# Checking basic statistics of numeric columns in POI Data
print("\nStatistics of Numeric Columns in POI Data:")
print(poi_data.describe())


# In[4]:


from shapely.geometry import Point, Polygon
from shapely.wkt import loads
import geopandas as gpd

# Assuming your 'geopoint' column looks like 'POINT(latitude longitude)'
mobility_data['longitude'] = mobility_data['geopoint'].apply(lambda x: float(x.split('(')[1].split()[0]))
mobility_data['latitude'] = mobility_data['geopoint'].apply(lambda x: float(x.split()[1].split(')')[0]))

# Create Shapely Point geometries
mobility_data['geometry'] = mobility_data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

# Drop the temporary 'latitude' and 'longitude' columns if needed
mobility_data.drop(['latitude', 'longitude'], axis=1, inplace=True)

# Create GeoDataFrame for mobility data
gdf_mobility = gpd.GeoDataFrame(mobility_data, geometry='geometry')

# Create GeoDataFrame for POI data
poi_data['geometry'] = poi_data['geopolygon_shape'].apply(lambda x: loads(x))
gdf_poi = gpd.GeoDataFrame(poi_data, geometry='geometry')

# Display the first few rows of each GeoDataFrame
print("GeoDataFrame for Mobility Data:")
print(gdf_mobility.head())

print("\nGeoDataFrame for POI Data:")
print(gdf_poi.head())


# In[16]:


import pandas as pd
from shapely.geometry import Point

# Assuming your 'geopoint' column looks like 'POINT(latitude longitude)'
mobility_data['longitude'] = mobility_data['geopoint'].apply(lambda x: float(x.split('(')[1].split()[0]))
mobility_data['latitude'] = mobility_data['geopoint'].apply(lambda x: float(x.split()[1].split(')')[0]))

# Create Shapely Point geometries
mobility_data['geometry'] = mobility_data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
# Drop the temporary 'latitude' and 'longitude' columns if needed
mobility_data.drop(['latitude', 'longitude'], axis=1, inplace=True)
mobility_data.head()


# In[6]:


from shapely.geometry import Point, Polygon
from shapely.wkt import loads  # Add this import statement
from geopandas import GeoDataFrame, sjoin

#geopolygon_shape
poi_data['geometry'] = poi_data['geopolygon_shape'].apply(lambda x: loads(x))

poi_data.head()


# In[7]:


import geopandas as gpd
from shapely.wkt import loads

# Assuming your 'geopoint' column looks like 'POINT(latitude longitude)'
# This code extracts latitude and longitude from the 'geopoint' column and creates new columns 'longitude' and 'latitude' in the mobility_data DataFrame.
# Creating Shapely Point Geometries from Latitude and Longitude:
mobility_data['longitude'] = mobility_data['geopoint'].apply(lambda x: float(x.split('(')[1].split()[0]))
mobility_data['latitude'] = mobility_data['geopoint'].apply(lambda x: float(x.split()[1].split(')')[0]))



# Create Shapely Point geometries
# Shapely Point geometries are created based on the latitude and longitude columns, and a new column 'geometry' is added to the mobility_data DataFrame.
# Creating GeoDataFrame for Mobility Data:
mobility_data['geometry'] = mobility_data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

# Create GeoDataFrame for mobility data
# The gdf_mobility GeoDataFrame is created using the mobility_data DataFrame, and the 'geometry' column is specified.
# Creating Shapely Point Geometries from 'geopolygon_shape' in poi_data:
gdf_mobility = gpd.GeoDataFrame(mobility_data, geometry='geometry')

# Assuming 'geopolygon_shape' is the geometry column in poi_data
# Shapely geometries are created from the 'geopolygon_shape' column using the loads function, and a new column 'polygon_geometry' is added to the poi_data DataFrame.
# Creating GeoDataFrame for POI Data:
poi_data['polygon_geometry'] = poi_data['geopolygon_shape'].apply(lambda x: loads(x))
gdf_poi = gpd.GeoDataFrame(poi_data, geometry='geometry')


# The gdf_poi GeoDataFrame is created using the poi_data DataFrame, and the 'geometry' column is specified.
# Perform spatial join
join_result = gpd.sjoin(gdf_mobility, gdf_poi, how="right", op="intersects")

# Sort the result in descending order by 'estimated_visits'
join_result = join_result.sort_values(by='estimated_visits', ascending=False)

# Display the result
join_result.head()



# In[8]:


# Save the result to a CSV file
join_result.to_csv(r'C:\Users\EmmaThiDieuNGUYEN\OneDrive - Xpollens\Desktop\Paper\join_result.csv', index=False)


# In[9]:


# Display only specific columns
selected_columns = ['cluster_id', 'week', 'estimated_visits', 'geometry','dwell_time','poi_id','poi_name','brand','naics_tier2_title','polygon_geometry']
result_to_display = join_result[selected_columns]

# Display the result
result_to_display


# In[42]:


import matplotlib.pyplot as plt

filtered_join_result = join_result[join_result['dwell_time'] > 0]

# Group by 'week' and 'brand', summing the 'estimated_visits' for each group
grouped_data = filtered_join_result.groupby(['week', 'naics_tier2_title'])['estimated_visits'].sum().reset_index()

# Pivot the data to have 'brand' as columns and 'week' as index
pivot_data = grouped_data.pivot(index='week', columns='naics_tier2_title', values='estimated_visits')

# Calculate the total estimated visits for each brand and sort by ascending order
brand_totals = pivot_data.sum(axis=0).sort_values()

# Sort the columns of pivot_data by the total estimated visits
pivot_data = pivot_data[brand_totals.index]

# Plotting the bar chart with ordered legend
ax = pivot_data.plot(kind='bar', stacked=True, figsize=(10, 6))
ax.set_ylabel('Estimated Visits')
ax.set_xlabel('Week')
ax.set_title('Estimated Visits by Brand and Week (Ascending Order)')

# Get the ordered legend labels
ordered_labels = brand_totals.index

# Create a legend with ordered labels
ax.legend(ordered_labels, title='naics_tier2_title', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()


# In[44]:


# Group by 'week' and 'brand', summing the 'estimated_visits' for each group
grouped_data = join_result.groupby(['week', 'brand'])['estimated_visits'].sum().reset_index()

# Get the top 5 brands for each week
top_brands_by_week = grouped_data.groupby('week').apply(lambda x: x.nlargest(5, 'estimated_visits')).reset_index(drop=True)

# Sort the values in descending order
top_brands_by_week = top_brands_by_week.sort_values(by=['week', 'estimated_visits'], ascending=[True, False])

# Pivot the data to have 'brand' as columns and 'week' as index
pivot_data = top_brands_by_week.pivot(index='week', columns='brand', values='estimated_visits')

# Plotting the bar chart
ax = pivot_data.plot(kind='bar', stacked=True, figsize=(10, 6))
ax.set_ylabel('Estimated Visits')
ax.set_xlabel('Week')
ax.set_title('Top 5 Brands by Estimated Visits Grouped by Week')

# Create a legend with ordered labels
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title='Brand', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()


# In[10]:


pip install --user --upgrade matplotlib


# In[37]:


import matplotlib.pyplot as plt

# Assuming you have GeoDataFrames poi_data and mobility_data
# Make sure they have the correct 'geometry' columns

filtered_join_result = join_result[join_result['dwell_time'] > 0]

fig, ax = plt.subplots(figsize=(10, 10))

# Plotting centroids where dwell_time > 0

filtered_join_result.plot(ax=ax, color='yellow', markersize=50)
gdf_poi.plot(ax=ax, alpha=0.5, edgecolor='b')


plt.show()



# In[ ]:




