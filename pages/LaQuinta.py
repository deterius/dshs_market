import pandas as pd
import streamlit as st
import datetime as dt
import numpy as np

df = pd.read_excel('./data/lq_test.xlsx')


# Streamlit app layout
st.title("Property Data Analysis")
st.write("Data Overview:")

# add price per sqr footage
df['Price Sqr Foot'] = df['price info amount value'] / df['sqft info amount value']


# Assuming you want to calculate the number of days from the current date
current_date = dt.datetime.now()
# Calculate the number of days
df['days since added to market'] = (current_date - df['date added to market']).dt.days

df = df[['property type',
         'beds value',
         'baths value',
         'price info amount value',
         'sqft info amount value',
         'lot size amount value',
         'date added to market',
         'date added to redfin',
         'year built year built value',
         'date of last sale',
         'Price Sqr Foot',
         'hoa dues amount value',
         'days since added to market'
         ]]
st.write(df)


# Select a subset of columns as default
default_columns = df.columns[:80].tolist()
selected_columns = st.multiselect('Select columns to display', df.columns, default=default_columns)


# Dropdown for property type
selected_prop_type = st.selectbox('Select Property Tiype', df['property type'].unique())
# Checkbox to filter out properties with HOA fees
exclude_hoa = st.checkbox('Exclude properties with HOA fees')

# Checkbox to enable filtering
remove_extremes = st.checkbox('Remove bottom and top 2% of prices')



# Filter the DataFrame based on the selection
filtered_df = df[df['property type'] == selected_prop_type]

if remove_extremes:
    # Calculate the 2nd and 98th percentiles
    low_threshold = df['price info amount value'].quantile(0.02)
    high_threshold = df['price info amount value'].quantile(0.98)

    # Filter the DataFrame
    filtered_df = df[(df['price info amount value'] > low_threshold) & (df['price info amount value'] < high_threshold)]
else:
    filtered_df = df

# Further filter to exclude properties with HOA fees if the checkbox is checked
if exclude_hoa:
    filtered_df = filtered_df[pd.isna(filtered_df['hoa dues amount value']) | (filtered_df['hoa dues amount value'] == 0)]



# Display the selected columns of the DataFrame
st.dataframe(filtered_df[selected_columns])

st.write(filtered_df.describe())

