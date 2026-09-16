import pandas as pd
import plotly.express as px
import streamlit as st
df = pd.read_csv('all_df.csv')
st.set_page_config(page_title = "My Sales 2019 Dashboard", page_icon=":new:",layout='wide')
st.sidebar.header("Please Filter Here:")
product_optionsList = st.sidebar.multiselect(
    "Select Product:",
    options = df['Product'].unique(),
    default = df['Product'].unique()[:5]
)
city_optionsList = st.sidebar.multiselect(
    "Select City:",
    options = df['City'].unique(),
    default = df['City'].unique()[:5]
)
month_optionsList = st.sidebar.multiselect(
    "Select Month:",
    options = df['Month'].unique(),
    default = df['Month'].unique()[:5]
)
st.title(":bar_chart: Sales Dashboard 2019")
st.markdown('#')
total_sales = df['Total'].sum()
unique_product = df['Product'].nunique()
left_col, right_col = st.columns(2)
with left_col:
    st.subheader('Total Sales')
    st.subheader(f'US $ {total_sales}')
with right_col:
    st.subheader('Number of Products')
    st.subheader(f'{unique_product}')
df_select = df.query("City == @city_optionsList and Product == @product_optionsList and Month == @month_optionsList")
a,b,c = st.columns(3)
sales_by_product = df_select.groupby('Product') ['Total'].sum().sort_values()
fig_sales_by_product = px.bar(
    sales_by_product,
    y = sales_by_product.index,
    x = sales_by_product.values,
    title = "Total by Product"
)
a.plotly_chart(fig_sales_by_product,use_container_width = True)

sales_by_city = df_select.groupby('City') ['Total'].sum().sort_values()
fig_sales_by_city = px.pie(
    sales_by_city,
    values = sales_by_city.values,
    names = sales_by_city.index,
    title = "Total by City"
)
b.plotly_chart(fig_sales_by_city,use_container_width = True)

sales_by_month = df_select.groupby('Month') ['Total'].sum().sort_values()
fig_sales_by_month = px.line(
    sales_by_month,
    x = sales_by_month.values,
    y = sales_by_month.index,
    title = "Total by Month"
)
c.plotly_chart(fig_sales_by_month,use_container_width = True)

d,e = st.columns(2)
fig_total_dist =px.histogram(
    df_select,
    x='Total',
    nbins=20,
    title = "Total Distribution"
)
d.plotly_chart(fig_total_dist,use_container_width = True)
fig_scatter = px.scatter(
    df_select,
    x='Day',
    y='QuantityOrdered',
    color = 'TimeInterval',
    title = "Quantity Ordered Pattern by Day"
)
e.plotly_chart(fig_scatter,use_container_width = True)
    