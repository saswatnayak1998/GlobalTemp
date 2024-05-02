import streamlit as st
import pandas as pd
import plotly.express as px

url = ""
data = pd.read_csv(url)

data.columns = data.columns.map(str)

st.title('Global Temperature Deviations')

selected_year = st.slider('Select Year', min_value=1961, max_value=2023, step=1)
selected_year = str(selected_year)  # Convert to string to match dataframe columns

fig = px.choropleth(
    data_frame=data,
    locations="ISO3",  
    color=selected_year,  
    hover_name="Country",  
    color_continuous_scale=px.colors.sequential.Plasma, 
    projection="natural earth", 
    title=f"Global Temperature Deviations in {selected_year}"
)
fig.update_geos(visible=False)  
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})  

st.plotly_chart(fig)
