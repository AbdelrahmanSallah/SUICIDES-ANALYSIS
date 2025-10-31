
import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(layout='wide', page_title='SUICIDES OVERVIEW' )
html_title = """<h1 style="color:white;text-align:center;"> SUICIDES Data Analysis </h1>"""
st.markdown(html_title, unsafe_allow_html=True)
df= pd.read_csv('cleaned_df.csv')
st.image("logo.jpg")
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio(
    "Choose a page:",
    ['🏠 Home', '📊 KPI Dashboard', '📈 Analytical Report']
)

if 'Home' in  page:
    st.dataframe(df)
    column_descriptions = {
        'country': 'Name of the country where the data was collected.',
        'year': 'Year of record (from 1985 to 2016).',
        'sex': 'Gender category: Male or Female.',
        'age': 'Age group category (e.g., 15-24 years, 35-54 years).',
        'suicides_no': 'Number of recorded suicides in that country, year, and group.',
        'population': 'Population of that specific demographic group (age + sex + country + year).',
        'suicides_per_100k': 'Calculated suicide rate per 100,000 people (suicides_no / population × 100,000).',
        'country-year': 'Combined identifier showing both country and year (e.g., "Canada1985").',
        'HDI for year': 'Human Development Index for that country and year (from 0 to 1). May have missing values.',
        'gdp_for_year ($)': 'Total Gross Domestic Product (GDP) for that country and year in USD. Example: "1,234,567,890".',
        'gdp_per_capita ($)': 'GDP per person (in USD), representing average wealth level.',
        'generation': 'Cultural generation group (e.g., Generation X, Silent, Boomers, Millennials).'
    }
  #  st.subheader("📘 Dataset Column Descriptions")
  #  for col, desc in column_descriptions.items():
    #    st.markdown(f"**{col}** — {desc}")

    st.subheader('Column Description as a TABLE VIEW')
    desc_df= pd.DataFrame(list(column_descriptions.items()),columns=["Column Name","Description"])
    st.table(desc_df)
elif 'KPI Dashboard' in page:
    # Basic KPIs

    total_countries= df['country'].nunique()
    total_suicide_no= df['suicides_no'].sum()
    max_year = df.groupby('year')['suicides_no'].sum().idxmax()
    max_year_value = df.groupby('year')['suicides_no'].sum().max()
    col1,col2,col3 = st.columns(3)
   
    col1.metric("🌍 Number of total countries is:", f"{total_countries:,}")
    col2.metric("💀 Total number of suicide from 1985 to 2016 is: ", f"{total_suicide_no:,}")
    col3.metric("📅 Highest Year", f"{max_year} ({max_year_value:,})")
    st.write('---')

    # PLOTLY
    # Yearly
    yearly_suicides = df.groupby('year')['suicides_no'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=yearly_suicides,x='year', y='suicides_no',title= 'no. Of suicides no per year ', text_auto= True))

    # TOP COUNTRIES
    top_countries = df.groupby('country')['suicides_no'].sum().reset_index().sort_values('suicides_no',ascending=False).head(10)
    st.plotly_chart(px.bar(data_frame=top_countries , x='country', y='suicides_no', title='Top 10 Countries by Total Suicides'))

# ENUFF FOR PAGE II

elif "Analytical" in page:
    min_year= df['year'].min()
    max_year= df['year'].max()

   # st.sidebar.number_input('Select the years you want to check', min_value= min_year, max_value= max_year,step =1)
    start_year, end_year = st.sidebar.slider("Select Year Range:", min_value=min_year, max_value=max_year, value=(min_year, max_year),step =1)
    df_filtered = df[(df['year']>= start_year) & (df.year <= end_year)]
    
    # Filter country per year

    All_countries = df_filtered.country.unique().tolist() + ['All countries']
    country= st.sidebar.selectbox("Select Country", All_countries)

    if  country != 'All countries': 
        df_filtered=df_filtered[df_filtered.country == country]
    st.dataframe(df_filtered)

