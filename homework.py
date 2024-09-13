import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image


data = pd.read_csv("demographics.csv")

logo = Image.open("aub_white.jpg")

st.image(logo)


st.title('Case Study: Distribution of the Lebanese Demographics')

st.header('Mahdi Husseini - MSBA 325')

st.warning(
    "This app is optimized for desktop viewing due to the wide nature of the visualizations, which may not fit well on smaller mobile screens. "
    "For the best experience, we recommend using a desktop, or if you're on a mobile device, enabling the 'Desktop site' option in your browser. "
    "Don't forget to check the sidebar to adjust the district selection as needed."
)

st.write('***')

st.subheader('Data')

st.data_editor(data)

st.write('***')

st.header('Boxplot of the distribution of Elders and youth across Districts')


selected = st.sidebar.multiselect('Districts', options=data['District'].unique(), default=data['District'].unique())


districts = data.groupby('District').agg({
    'Percentage of Women': 'sum',
    'Percentage of Men' : 'sum'
}).reset_index()


districts['Total'] = districts['Percentage of Women'] + districts['Percentage of Men']
districts['Percentage of Women'] = districts['Percentage of Women'] / districts['Total']
districts['Percentage of Men'] = districts['Percentage of Men'] / districts['Total']

districts.drop(columns='Total', axis=1, inplace=True)

boxp = data[['District', 'Percentage of Eldelry - 65 or more years ', 'Percentage of Youth - 15-24 years', 'Town']]

filtered = boxp[boxp['District'].isin(selected)]

############################################################ Boxplot ##############################################################################################################################################

cats = ['Youth', 'Elders vs Youth', 'Elders']

check = st.selectbox('Category', options=cats)

def interpreter(a):
    if a == 'Elders':
        return " The boxplot above shows the distribution of elderly individuals (65 years or older) across different Lebanese districts.\n We can observe that the average percentage of elderly people across most districts is **quite similar**.\n However, there are some notable outliers, with a few districts having lower-than-average percentages.\n For example, Jall ed-Dib in Matn has an exceptionally low percentage of elderly residents, with *0% elders* in that specific town."

    if a == 'Youth':
        return """The boxplot above illustrates the distribution of youth (15-24 years) across Lebanese districts.
                We can see that the spread of youth percentages is relatively consistent across most districts.
                However, districts like Baalbek and Mount Lebanon show higher outliers, while districts like Zgharta and Aley have lower outliers.
                Additionally, unlike the elderly distribution, the median youth percentages vary significantly across districts, suggesting a high variability
                in the youth population across Lebanon."""

    return """The boxplot above compares the distribution of both youth and elderly populations across Lebanese districts.
            It is clear that the median percentage of youth is generally higher than that of the elderly in most districts, indicating a predominantly young population in Lebanon.
            However, there are some exceptions where the percentage of elderly is notably higher than the youth population, such as in Qild Es Sabaa in the Baalbek-Hermel district."""



if check == 'Elders':

    fig = px.box(
        filtered, 
        x='District', 
        y='Percentage of Eldelry - 65 or more years ',
        color = 'District',
        hover_name = 'Town',
        title='Distribution of Elderly Population (65 or more years) by District',
        labels={'Percentage of Eldelry - 65 or more years ': "% of Elders (65+ year)"},
        points='all'
    )

    fig.update_layout(
        xaxis_tickangle=45
    )

    st.plotly_chart(fig)

    st.info(interpreter(check))

elif check  == 'Youth':
    fig = px.box(
        filtered, 
        x='District', 
        y='Percentage of Youth - 15-24 years',
        color = 'District',
        hover_name = 'Town',
        title='Distribution of Youth Population (15 - 24 years) by District',
        labels={'Percentage of Youth - 15-24 years': "% of Youth (15 - 24 years)"},
        points='all'
    )

    fig.update_layout(
        xaxis_tickangle=45
    )

    st.plotly_chart(fig)

    st.info(interpreter(check))

else:
    melted_data = filtered.melt(id_vars=['District', 'Town'], value_vars=['Percentage of Eldelry - 65 or more years ', 'Percentage of Youth - 15-24 years'], 
                        var_name='Age Group', value_name='Percentage')

    fig = px.box(
        melted_data, 
        x='District', 
        y='Percentage', 
        color='Age Group', 
        hover_name= 'Town',
        title='Distribution of Elderly vs Youth Population by District',
        labels={'Percentage': 'Population Percentage', 'Age Group': 'Age Group'}
    )
    fig.update_layout(
        xaxis_tickangle=45
    )

    st.plotly_chart(fig)

    st.info(interpreter(check))

st.write('***')

############################################################################################## Pie Chart #####################################################################################################################

def title_definer(x):
    if x == '1-3':
        return 'Distribution of families of 1-3 members across Lebanon'
    if x == '4-6':
        return 'Distribution of families of 4-6 members across Lebanon'
    
    return 'Distribution of families of 7+ members across Lebanon'


st.header('Piechart of the distribution of families (By members) across districts')

fam = data[['District', 'family']]

filtered_fam = fam[fam['District'].isin(selected)]

familia = ['1-3', '4-6', '7+']

fms = st.select_slider('Family Members', familia)

selected_fam = filtered_fam[filtered_fam['family'] == fms]

counted = selected_fam.groupby('District').size().reset_index(name = 'freq')

def pie_inter(b):
    if b == '1-3':
       return  """In the above pie_chart, we can see the percentage of the 1-3 family members across districts, where although Keserwan is the leading with 9% of the 1-3 family category, the districts following it aren't that much far from it's score, which almost makes the pie_chart seem sliced into equal parts, insighting that approximately all cities in lebanon has on average the same distribution of families of 1-3 members across all districts"""

    if b == '4-6':
        return """This pie_chart display the percentage of 4-6 family members, we can distinguish that Akkar is the leading district with a percentage of 14%, with Mount Lebanon as 8%, and the following districts averaged as around 3% - 5%, indicating that the cities in Akkar has the most distribution of families with 4-6 members, and the other districts have approximately the same distribution percentage (with Tripoli, Hermel, and Bcharri as 0.5%, 1% and 1.5% respectively)"""
    return """The percentage od distribution of familes with more thean 7 members is diplayed in the above pie-chart, where again Akkar leads the way but exponentially this time with a 59.4% of cities within it having this family category alone,followed by Miniyeha at 12.5%, then Baalbek-Hermel at 9.38%, lastly we have the remaining 6 districts with the same percentage of 3.13% each(note as observed only 9 districts out of 25 has cities with families of more than 7 members). Knowing that there's only a total 32 cities with familes having more than 7 members on average, we can still derive that Akkar is the leading district in this category, followed by miniyeha and baalbel-hermel as second and third, then Districts from the south having equal percentage( 1 city of this category for each district). We can assume by that also that districts located in poor areas have more family members (wealth is inversely proportional to family members in Lebanon)"""

fg = px.pie(
    counted,
    values = 'freq',
    names = 'District',
    title= title_definer(fms)
)

st.plotly_chart(fg)

st.info(pie_inter(fms))
