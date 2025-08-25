import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Zomato Restaurant Insights Dashboard")

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/harshala2429/Zomato_new/main/zomato_clean.csv")

# Sidebar filters
st.sidebar.header("Filter Options")
city_options = ["All"] + df['location'].dropna().unique().tolist()
cuisine_options = ["All"] + df['cuisines'].dropna().unique().tolist()

selected_city = st.sidebar.selectbox("Select City", city_options)
selected_cuisine = st.sidebar.selectbox("Select Cuisine", cuisine_options)

# Apply filters
filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df['location'] == selected_city]
if selected_cuisine != "All":
    filtered_df = filtered_df[filtered_df['cuisines'].str.contains(selected_cuisine, case=False, na=False)]

# Show filtered data
st.subheader("Filtered Restaurants")
st.dataframe(filtered_df[['name', 'location', 'cuisines', 'rate', 'approx_cost(for two people)']].sort_values(by='rate', ascending=False))

# Top 10 Restaurants by Rating
st.subheader("Top 10 Restaurants by Rating")
top_restaurants = filtered_df.sort_values(by='rate', ascending=False).head(10)
st.bar_chart(top_restaurants.set_index('name')['rate'])

# Rating Distribution
st.subheader("Rating Distribution")
fig1 = px.histogram(filtered_df, x='rate', nbins=10, title='Rating Distribution')
st.plotly_chart(fig1)

# Cuisine Popularity
st.subheader("Cuisine Popularity")
cuisine_count = filtered_df['cuisines'].value_counts().reset_index()
cuisine_count.columns = ['cuisines', 'Count']
fig2 = px.pie(cuisine_count, names='cuisines', values='Count', title='Cuisine Distribution')
st.plotly_chart(fig2)

# Cost vs Rating Scatter
st.subheader("Cost vs Rating")
fig3 = px.scatter(filtered_df, x='approx_cost(for two people)', y='rate', color='cuisines', hover_data=['name'], title='Cost vs Rating')
st.plotly_chart(fig3)
