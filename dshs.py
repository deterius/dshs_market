import pandas as pd
import streamlit as st
import datetime as dt
# df = pd.read_excel('data/dshs_test2.xlsx')
df = pd.read_csv('data/dshs_test.csv')

# Streamlit app layout
st.title("Property Data Analysis")

# add price per sqr footage
df['Price Sqr Foot'] = df['price info amount value'] / df['sqft info amount value']


# Assuming you want to calculate the number of days from the current date
current_date = dt.datetime.now()
# Calculate the number of days
df['date added to market'] = pd.to_datetime(df['date added to market'])
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
         'days since added to market',
         'sold',
         'url'
         ]]


# Select a subset of columns as default
default_columns = df.columns[:80].tolist()
selected_columns = st.multiselect('Select columns to display', df.columns, default=default_columns)


# Dropdown for property type
selected_prop_type = st.selectbox('Select Property Tiype', df['property type'].unique())
# Checkbox to filter out properties with HOA fees
exclude_hoa = st.checkbox('Exclude properties with HOA fees')

# Filter the DataFrame based on the selection
filtered_df = df[df['property type'] == selected_prop_type]

# Further filter to exclude properties with HOA fees if the checkbox is checked
if exclude_hoa:
    filtered_df = filtered_df[pd.isna(filtered_df['hoa dues amount value']) | (filtered_df['hoa dues amount value'] == 0)]



# Display the selected columns of the DataFrame
st.dataframe(filtered_df[selected_columns])
st.header('Market Analytic Details')
st.write(filtered_df.describe())

#---- filter the baths and beds
st.header('Average Price for House')

# Streamlit widgets to select the number of beds and baths
selected_beds = st.selectbox('Select number of bedrooms', filtered_df['beds value'].unique())
selected_baths = st.selectbox('Select number of bathrooms', filtered_df['baths value'].unique())



# Filter the DataFrame based on the selected criteria
filtered_by_criteria = filtered_df[
    (filtered_df['beds value'] == selected_beds) &
    (filtered_df['baths value'] == selected_baths)
]

# Slider for selecting lot size range
min_lot_size, max_lot_size = st.slider(
    'Select lot size range',
    min_value=int(filtered_by_criteria['lot size amount value'].min()),
    max_value=int(filtered_by_criteria['lot size amount value'].max()),
    value=(int(filtered_by_criteria['lot size amount value'].min()), int(filtered_by_criteria['lot size amount value'].max()))
)

# Slider for selecting home size range
min_house_size, max_house_size = st.slider(
    'Select sqft info range',
    min_value=int(filtered_by_criteria['sqft info amount value'].min()),
    max_value=int(filtered_by_criteria['sqft info amount value'].max()),
    value=(int(filtered_by_criteria['sqft info amount value'].min()), int(filtered_by_criteria['sqft info amount value'].max()))
)

# Filter the DataFrame based on the selected criteria
filtered_by_criteria = filtered_by_criteria[
    (filtered_by_criteria['lot size amount value'] >= min_lot_size) &
    (filtered_by_criteria['lot size amount value'] <= max_lot_size) &
    (filtered_by_criteria['sqft info amount value'] >= min_house_size) &
    (filtered_by_criteria['sqft info amount value'] <= max_house_size)
]

# Calculate the average price
if not filtered_by_criteria.empty:
    average_price = filtered_by_criteria['price info amount value'].mean()
    st.write(f"Average price for homes with {selected_beds} bedrooms, {selected_baths} bathrooms, lot size between {min_lot_size} and {max_lot_size}, and house size between {min_house_size} and {max_house_size}: ${average_price:.2f}")
    col1, col2 = st.columns(2)
    col1.subheader('Average Price:')
    col2.subheader(f"${average_price:.2f}")
else:
    st.write("No homes match the selected criteria.")

st.dataframe(filtered_by_criteria)



#  ----------------------------------------------
# Show sold homes only
sold_df = filtered_df[filtered_df['sold'] == True]
st.header('SOLD/PENDING')


# Function to convert URL to a clickable link
def make_clickable(url, name):
    return f'<a target="_blank" href="https://www.redfin.com{url}">{name}</a>'

# Apply the function to the DataFrame
sold_df['link'] = sold_df.apply(lambda row: make_clickable(row['url'], row['property type']), axis=1)

# Convert DataFrame to HTML and use st.markdown to display it with clickable links
st.markdown(sold_df.to_html(escape=False, index=False), unsafe_allow_html=True)