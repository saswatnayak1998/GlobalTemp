import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

url = "https://raw.githubusercontent.com/saswatnayak1998/GlobalTemp/main/ClimateChangeStats.csv"
data = pd.read_csv(url)

data.columns = data.columns.map(str)

year_columns = [col for col in data.columns if col.isdigit()]
data_long = data.melt(id_vars=['Country', 'ISO3'], value_vars=year_columns,
                      var_name='Year', value_name='Temperature Deviation')

data_long.dropna(subset=['Temperature Deviation'], inplace=True)

st.title('Global Temperature Deviations - Animated Map - Saswat K Nayak')

fig = px.choropleth(
    data_frame=data_long,
    locations="ISO3",
    color="Temperature Deviation",
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale=px.colors.sequential.Plasma,
    projection="natural earth",
    title="Global Temperature Deviations Over the Years"
)
fig.update_layout(margin={"r":0, "t":40, "l":0, "b":0})
st.plotly_chart(fig, use_container_width=True)

country_selected = st.selectbox("Select or type a country", options=data['Country'].unique(), format_func=lambda x: x)

if country_selected:
    country_data = data[data['Country'] == country_selected]
    temp_deviations = country_data[year_columns].transpose()
    temp_deviations.columns = ['Temperature Deviation']
    temp_deviations['Year'] = temp_deviations.index.astype(int)
    fig2 = px.line(temp_deviations, x='Year', y='Temperature Deviation', title=f'Temperature Deviations Over the Years for {country_selected}')
    st.plotly_chart(fig2)

slopes = {}
for country in data['Country'].unique():
    country_data = data[data['Country'] == country]
    country_data = country_data[year_columns].transpose()
    country_data.columns = ['Temperature Deviation']
    country_data['Year'] = country_data.index.astype(int)
    country_data.dropna(inplace=True) 

    if len(country_data['Year']) > 1:  
        slope, _ = np.polyfit(country_data['Year'], country_data['Temperature Deviation'], 1)
        slopes[country] = slope

sorted_slopes = sorted(slopes.items(), key=lambda x: x[1], reverse=True)
top_countries = sorted_slopes[:10]
lowest_countries = sorted_slopes[-10:] if sorted_slopes else None

st.subheader("Top 10 Countries with the Highest Increase in Temperature Deviations")
for country, slope in top_countries:
    st.write(f"{country}: {slope:.2f}°/year")

st.subheader("Top 10 Countries with the Lowest Increase in Temperature Deviations")
for country, slope in lowest_countries:
    st.write(f"{country}: {slope:.2f}°/year")