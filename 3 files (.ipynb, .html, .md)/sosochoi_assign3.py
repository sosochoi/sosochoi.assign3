#!/usr/bin/env python
# coding: utf-8

# # Assignment 3: A Baby Project
# # Sephora Skincare Reviews Data Analysis
# ## 1. Opens up the product_info datafile.
# ### 1.1 Load the product_info Data

# In[9]:


# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data
df = pd.read_csv('product_info.csv')


# ### 1.2 Overview of Data Set 

# ### Dataset Name: Sephora Skincare Reviews
# **Source**: Kaggle
# 
# **Content**:
# - Customer reviews for skincare and makeup products sold at Sephora
# - Includes product names and ratings
# - Pricing details (original price, sale price)
# - Additional attributes such as ingredients, variation types, and sizes
# - Availability indicators (limited edition, online only, out of stock)
# - Consumer engagement metrics (loves count, total reviews)
# 
# **Key Statistical Insights**
# - **No. of columns**: 27
# - **No. of rows**: 8,494
# - **Unique Products**: 8,415
# - **Unique Brands**: 304
# - **Brand with Most Products**: SEPHORA COLLECTION (Number of Products: 352)
# 
# Notable **Missing Values** in the dataset include:
# - **variation_desc**: 7244 missing values (85.28%)
# - **value_price_usd**: 8043 missing values (94.69%)
# - **sale_price_usd**: 8224 missing values (96.82%)
# - **child_max_price**: 5740 missing values (67.58%)
# - **child_min_price**: 5740 missing values (67.58%)
#  
# 

# ### 1.2.1 Summary Statistics

# In[10]:


# 1.2 Data Overview
summary_statistics = data.describe(include='all')
summary_statistics


# ### 1.2.2 Missing Data Summary

# In[11]:


# Calculate the number of missing values for each column
missing_values_count = data.isnull().sum()

# Get the data types of each column
data_types = data.dtypes

# Combine all the required details into a single DataFrame
missing_data_summary = pd.DataFrame({
    'Column': data.columns,
    'Dtype': data_types,
    'Missing Count': missing_values_count,
    'Missing Percentage (%)': (missing_values_count / data.shape[0]) * 100
})

# Keep the original order of columns in the dataset
missing_data_summary = missing_data_summary.reset_index(drop=True)

# Display the full summary
print("Missing Data Summary")
print(missing_data_summary)


# ## 2. Exploratory Data Analysis (EDA) - Summaries

# ### 2.1 Average Rating for Each Product Category
# - **Objective**: Calculate average ratings for products by brand.
# - **Insight**: Identifies top-performing brands based on customer ratings.

# In[32]:


# Pivot table for average rating by brand name
avg_rating_by_brand = df.groupby('brand_name')['rating'].mean().reset_index()

# Sort the results from high to low ratings
avg_rating_by_brand = avg_rating_by_brand.sort_values(by='rating', ascending=False)

# Print the title and the DataFrame
print("Average Rating by Brand Name:\n")
print(avg_rating_by_brand)


# ### 2.2 List of Products with Ratings Above 4.5 and Minimum Lovescount = 200000
# - **Objective**: Filter products with high ratings and significant popularity.
# - **Insight**: Highlights successful, high-quality products in the market.

# In[33]:


# Define criteria
rating_threshold = 4.5
min_loves_count = 200000

# Filter products based on criteria
filtered_products = df[
    (df['rating'] > rating_threshold) &
    (df['loves_count'] >= min_loves_count)
].copy()  # Create a copy to avoid SettingWithCopyWarning

# Sort by rating
filtered_products = filtered_products.sort_values(by='rating', ascending=False)

print("List of Products with Ratings Above 4.5 and Minimum Lovescount = 200000\n")

# Display relevant columns
print(filtered_products[['brand_name', 'product_name', 'rating', 'loves_count']])


# ### 2.3 Average Price by Category and New Products
# - **Objective**: Analyze average prices by product category and new status.
# - **Insight**: Reveals pricing trends, aiding marketing and inventory decisions.

# In[34]:


# Create a pivot table to calculate average price by primary category and new status
pivot_avg_price = df.pivot_table(values='price_usd', index='primary_category', columns='new', aggfunc='mean', fill_value=0)

# Rename columns for clarity
pivot_avg_price.columns = ['Not New', 'New']

# Resetting index to make the table more user-friendly
pivot_avg_price.reset_index(inplace=True)

# Print the title
print("Average Price by Primary Category and New Status\n")

# Display the pivot table
print(pivot_avg_price)


# ## 3. Exploratory Data Analysis (EDA) - Charts

# ### 3.1 Histogram: Distribution of Customer Ratings for Skincare Products
# - **Objective**: Visualize customer rating distribution for skincare products.
# - **Insight**: Illustrates overall customer satisfaction levels across all products, providing a comprehensive view of rating trends 

# In[41]:


# Calculate average ratings by brand
top_brands = df.groupby('brand_id')['rating'].mean().reset_index()

# Sort by average rating and get the top 10
top_brands = top_brands.sort_values(by='rating', ascending=False).head(10)

# Plotting
plt.figure(figsize=(10, 6))
sns.histplot(df['rating'], bins=10, kde=True)  # Ensure 'df' is used if 'data' is not defined
plt.title('Distribution of Customer Ratings for Skincare Products')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)  # Dashed line, less bold
plt.show()


# ### 3.2 Bar Chart: Average Loves Count by Primary Category
# - **Objective**: Compare average loves counts across product categories.
# - **Insight**: Indicates customer loyalty and helps focus marketing efforts.

# In[39]:


# 2.2 Calculate average loves count by primary category
average_loves_count_by_category = df.groupby('primary_category')['loves_count'].mean().sort_values(ascending=False)

# Plotting the bar chart
plt.figure(figsize=(12, 6))
average_loves_count_by_category.plot(kind='bar', color='lightgreen')
plt.title('Average Loves Count by Primary Category')
plt.xlabel('Primary Category')
plt.ylabel('Average Loves Count')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()  # Adjust layout to make room for labels
plt.show()


# ### 3.3 Pie Chart: Proportion of Sephora Exclusive Products
# - **Objective**: Visualize the share of exclusive vs. non-exclusive products.
# - **Insight**: Informs inventory and marketing strategies regarding exclusivity.

# In[38]:


# Count the number of exclusive and non-exclusive products
sephora_exclusive_count = df['sephora_exclusive'].value_counts()

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(sephora_exclusive_count, labels=sephora_exclusive_count.index, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightcoral'])
plt.title('Proportion of Sephora Exclusive Products')
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
plt.show()


# ### 3.4 Sephora Skincare Reviews Dataset Analysis Summary
# The **Sephora Skincare Reviews** dataset offers valuable insights into skincare products, emphasizing customer ratings and preferences. 
# Key analyses include:
# 
# - **Average Ratings**: Identifies top-performing brands based on customer feedback.
# - **High-Quality Products**: Highlights products with ratings above 4.5 and a minimum loves count, indicating significant popularity and market success.
# - **Pricing Trends**: Analyzes average prices by product category, aiding marketing strategies and inventory management.
# - **Customer Satisfaction**: Visualizes the distribution of customer ratings, reflecting overall satisfaction levels with various products.
# - **Customer Loyalty**: Compares average loves counts across categories, indicating levels of brand loyalty among consumers.
# - **Product Exclusivity**: Shows the proportion of exclusive versus non-exclusive products, informing inventory and targeted marketing initiatives.
# 
