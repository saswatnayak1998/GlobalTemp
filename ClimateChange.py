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

global_min = data_long['Temperature Deviation'].min()
global_max = data_long['Temperature Deviation'].max()

st.title('Global Temperatures - Saswat K Nayak')

fig = px.choropleth(
    data_frame=data_long,
    locations="ISO3",
    color="Temperature Deviation",
    hover_name="Country",
    animation_frame="Year",
    color_continuous_scale=px.colors.sequential.Plasma,
    range_color=[global_min, global_max],  
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

st.subheader("Top 10 Countries with the Highest Increase in Temperature")
for country, slope in top_countries:
    st.write(f"{country}: {slope:.2f}°/year")

st.subheader("Top 10 Countries with the Lowest Increase in Temperature")
for country, slope in lowest_countries:
    st.write(f"{country}: {slope:.2f}°/year")




url = "https://raw.githubusercontent.com/saswatnayak1998/GlobalTemp/main/ClimateChangeStats.csv"
data = pd.read_csv(url)

data.columns = data.columns.map(str)

slopes = {}
year_columns = [col for col in data.columns if col.isdigit()]
for country in data['Country'].unique():
    country_data = data[data['Country'] == country]
    country_data = country_data[year_columns].transpose()
    country_data.columns = ['Temperature Deviation']
    country_data['Year'] = country_data.index.astype(int)
    country_data.dropna(inplace=True)

    if len(country_data['Year']) > 1:
        slope, _ = np.polyfit(country_data['Year'], country_data['Temperature Deviation'], 1)
        slopes[country] = slope

top_countries = sorted_slopes[:100]
lowest_countries = sorted_slopes[-100:]

data['Slope'] = data['Country'].apply(lambda x: slopes.get(x, None))
data['Highlight'] = data['Country'].apply(lambda x: 'Top 100: Highest Temperature Increase' if x in [i[0] for i in top_countries] else ('Bottom 100 Lowest Temperature Increase' if x in [i[0] for i in lowest_countries] else 'Other'))

fig = px.choropleth(
    data_frame=data,
    locations="ISO3",
    color="Highlight",
    hover_name="Country",
    hover_data=["Slope"],
    color_discrete_map={'Top 100: Highest Temperature Increase': 'red', 'Bottom 100 Lowest Temperature Increase': 'blue', 'Other': 'lightgrey'},
    projection="natural earth",
    title="Global Temperature Increase Map"
)

fig.update_layout(margin={"r":0, "t":40, "l":0, "b":0}, title_font=dict(size=24),  
    font=dict(size=22),  
    legend_title_font_size=24,  
    legend_font_size=22)
st.plotly_chart(fig, use_container_width=True)

data.columns = data.columns.map(str)

# Calculate slopes for all countries
slopes = {}
year_columns = [col for col in data.columns if col.isdigit()]
for country in data['Country'].unique():
    country_data = data[data['Country'] == country]
    country_data = country_data[year_columns].transpose()
    country_data.columns = ['Temperature Deviation']
    country_data['Year'] = country_data.index.astype(int)
    country_data.dropna(inplace=True)  

    if len(country_data['Year']) > 1:
        slope, _ = np.polyfit(country_data['Year'], country_data['Temperature Deviation'], 1)
        slopes[country] = slope

# Streamlit app layout
slope_values = list(slopes.values())  # Extract just the slope values
fig = px.histogram(slope_values, nbins=40, labels={'value': 'Slope'}, title="Histogram of Rate of Temperature Change", )
fig.update_layout(
    title=dict(text='Histogram of Rate of Temperature Change', font=dict(size=30)), # Center and increase title size

    xaxis_title="Slope of Temperature Increase",
    yaxis_title="Count",
    xaxis=dict(
        title_font=dict(size=24),  # Font size for x-axis title
        tickfont=dict(size=22)     # Font size for x-axis ticks
    ),
    yaxis=dict(
        title_font=dict(size=24),  
        tickfont=dict(size=22)     
    )
)
st.plotly_chart(fig, use_container_width=True)

# Display the choropleth map as optional
st.subheader('Optional Global Map')
if st.checkbox('Show Map'):
    # Prepare data for the choropleth map
    data['Slope'] = data['Country'].apply(lambda x: slopes.get(x, None))
    fig_map = px.choropleth(
        data_frame=data,
        locations="ISO3",
        color="Slope",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="natural earth",
        title="Global Temperature Deviations Slopes"
    )
    fig_map.update_layout(margin={"r":0, "t":40, "l":0, "b":0}, )
    st.plotly_chart(fig_map, use_container_width=True)