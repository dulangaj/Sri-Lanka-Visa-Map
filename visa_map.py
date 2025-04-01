import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import iso3166

# Set page configuration
st.set_page_config(layout="wide", page_title="Visa-Free Travel Map")

# App title
st.title("🗺️ Visa-Free Travel Map")
st.subheader("Countries Sri Lankans can visit without a visa")

# Function to get visa-free countries for Sri Lanka
@st.cache_data
def get_visa_free_countries():
    """Get visa-free countries for Sri Lankan passport holders"""
    try:
        # Path to cached data
        cache_file = "visa_free_countries.json"
        
        # If we have cached data, use it
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # Hard-coded lists from https://visaindex.com/visa-requirement/sri-lanka-passport-visa-free-countries-list/
        # 1 April 2025
        visa_free_countries = [
            "Bahamas", "Barbados", "British Virgin Islands", "Cook Islands", "Dominica",
            "Gambia", "Grenada", "Haiti", "Kiribati", "Lesotho", "Malawi",
            "Micronesia", "Montserrat", "Rwanda", "Singapore", "St. Kitts and Nevis",
            "St. Vincent and the Grenadines", "Tajikistan", "Thailand", "Vanuatu", "Sri Lanka"
        ]
        
        visa_on_arrival = [
            "Bolivia", "Burundi", "Camnodia", "Cape Verde", "Comoros",
            "Djibouti", "Guinea-Bissau", "Laos", "Madagascar", "Maldives", "Mauritius", 
            "Nepal", "Niue", "Palau", "Samoa", "Seychelles", "Sierra Leone",
            "Tanzania", "Timor-Leste", "Tuvalu"
        ]
        
        e_visa = [
            "Kenya", "Pakistan", "Albania", "Antigua and Barbuda", "Australia",
            "Azerbaijan", "Bahrain", "Benin", "Bhutan", "Botswana", "Burkina Faso",
            "Cameroon", "Colombia", "Congo, Democratic Republic of the", 
            "Côte d'Ivoire", "Ecuador", "El Salvador", "Equatorial Guinea", 
            "Ethiopia", "Fiji", "Gabon", "Guinea", "Hong Kong", "India", "Indonesia",
            "Iran", "Iraq", "Kazakhstan", "Kyrgyzstan", "Libya",
            "Malaysia", "Mauritania", "Moldova", "Mozambique", 
            "Myanmar", "Namibia", "Nigeria", "Oman", 
            "Qatar", "Sao Tome and Principe", "South Sudan", "St. Helena", "Suriname",
            "Syria", "Togo", "Uganda", "United Arab Emirates", "Uzbekistan",
            "Vietnam", "Zambia", "Zimbabwe"
        ]
        
        result = {
            "visa_free": visa_free_countries,
            "visa_on_arrival": visa_on_arrival,
            "e_visa": e_visa
        }
        
        # Cache the data
        with open(cache_file, 'w') as f:
            json.dump(result, f)
            
        return result
    except Exception as e:
        st.error(f"Error getting visa-free countries: {e}")
        return {"visa_free": [], "visa_on_arrival": [], "e_visa": []}

# Get ISO codes for countries
@st.cache_data
def get_country_iso_codes():
    """Get ISO3 codes for countries"""
    # Create a mapping from country name to ISO3 code
    country_iso_mapping = {}
    
    for country in iso3166.countries:
        name = country.name
        iso3 = country.alpha3
        country_iso_mapping[name] = iso3
        # Add some common country name variations
        if name == "United States of America":
            country_iso_mapping["United States"] = iso3
            country_iso_mapping["USA"] = iso3
        elif name == "Russian Federation":
            country_iso_mapping["Russia"] = iso3
        elif name == "United Kingdom of Great Britain and Northern Ireland":
            country_iso_mapping["United Kingdom"] = iso3
            country_iso_mapping["UK"] = iso3
        elif name == "Korea, Republic of":
            country_iso_mapping["South Korea"] = iso3
        elif name == "Korea, Democratic People's Republic of":
            country_iso_mapping["North Korea"] = iso3
        elif name == "Venezuela, Bolivarian Republic of":
            country_iso_mapping["Venezuela"] = iso3
        elif name == "Tanzania, United Republic of":
            country_iso_mapping["Tanzania"] = iso3
        elif name == "Viet Nam":
            country_iso_mapping["Vietnam"] = iso3
        elif name == "Syrian Arab Republic":
            country_iso_mapping["Syria"] = iso3
        elif name == "Iran, Islamic Republic of":
            country_iso_mapping["Iran"] = iso3
        elif name == "Bolivia, Plurinational State of":
            country_iso_mapping["Bolivia"] = iso3
        elif name == "Lao People's Democratic Republic":
            country_iso_mapping["Laos"] = iso3
        elif name == "Timor-Leste":
            country_iso_mapping["East Timor"] = iso3
        elif name == "Cabo Verde":
            country_iso_mapping["Cape Verde"] = iso3
            
    # Add missing countries or special regions
    country_iso_mapping["Macao"] = "MAC"
    country_iso_mapping["Macau"] = "MAC"
    
    return country_iso_mapping

# Get visa data and country ISO codes
visa_data = get_visa_free_countries()
country_iso_mapping = get_country_iso_codes()

# Prepare data for visualization
countries_df = pd.DataFrame({
    'country': list(country_iso_mapping.keys()),
    'iso_alpha': [country_iso_mapping[country] for country in country_iso_mapping.keys()]
})

# Add visa status
countries_df['visa_status'] = 'Visa Required'

# Mark visa-free countries
for country in visa_data['visa_free']:
    for idx, row in countries_df.iterrows():
        if country.lower() in row['country'].lower():
            countries_df.at[idx, 'visa_status'] = 'Visa Free'

# Mark visa on arrival countries
for country in visa_data['visa_on_arrival']:
    for idx, row in countries_df.iterrows():
        if country.lower() in row['country'].lower():
            countries_df.at[idx, 'visa_status'] = 'Visa on Arrival'

# Mark e-visa countries
for country in visa_data['e_visa']:
    for idx, row in countries_df.iterrows():
        if country.lower() in row['country'].lower():
            countries_df.at[idx, 'visa_status'] = 'e-Visa'

# Create color map
color_map = {
    'Visa Free': '#00CC96',  # Green
    'Visa on Arrival': '#FFA15A',  # Orange
    'e-Visa': '#636EFA',  # Blue
    'Visa Required': '#EF553B'  # Red
}

# Create the choropleth map using Plotly's built-in country data
fig = px.choropleth(
    countries_df,
    locations='iso_alpha',
    color='visa_status',
    color_discrete_map=color_map,
    projection="natural earth",
    labels={'visa_status': 'Visa Status'},
    hover_name='country'
)

# Update layout for better visualization
fig.update_geos(
    showcoastlines=True,
    coastlinecolor="Black",
    showland=True,
    landcolor="LightGray",
    showocean=True,
    oceancolor="LightBlue",
    showlakes=True,
    lakecolor="LightBlue",
    showcountries=True,
    countrycolor="Black",
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=600,
)

# Display the map
st.plotly_chart(fig, use_container_width=True)

# Display the legend
st.markdown("### Visa Status Legend")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div style='background-color: {color_map['Visa Free']}; padding: 10px; border-radius: 5px;'>🟢 Visa Free ({len(visa_data['visa_free'])} countries)</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='background-color: {color_map['Visa on Arrival']}; padding: 10px; border-radius: 5px;'>🟠 Visa on Arrival ({len(visa_data['visa_on_arrival'])} countries)</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='background-color: {color_map['e-Visa']}; padding: 10px; border-radius: 5px;'>🔵 e-Visa ({len(visa_data['e_visa'])} countries)</div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div style='background-color: {color_map['Visa Required']}; padding: 10px; border-radius: 5px;'>🔴 Visa Required</div>", unsafe_allow_html=True)

# Display the list of countries
with st.expander("View List of Visa-Free Countries"):
    st.markdown("### Visa-Free Countries")
    st.write(", ".join(sorted(visa_data['visa_free'])))
    
    st.markdown("### Visa on Arrival Countries")
    st.write(", ".join(sorted(visa_data['visa_on_arrival'])))
    
    st.markdown("### e-Visa Countries")
    st.write(", ".join(sorted(visa_data['e_visa'])))

# Add info
st.markdown("---")
st.markdown("""
**Note:** This data is for demonstration purposes only. Always verify visa requirements with official sources before traveling.
""") 