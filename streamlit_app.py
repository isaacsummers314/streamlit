from sre_constants import GROUPREF_EXISTS
import streamlit
import pandas as pd

import requests

import snowflake.connector

from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.header('Breakfast Menu')
streamlit.text('😅Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected] if fruits_selected else my_fruit_list

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# create function
def get_fruity_vice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    return pd.json_normalize(fruityvice_response.json())


# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    if fruit_choice := streamlit.text_input('What fruit would you like information about?'):
        fv_result = get_fruity_vice_data(fruit_choice)       
        streamlit.dataframe(fv_result)
    else:
        streamlit.error("Please select a fruit to get information.")
except URLError as e:
    streamlit.error()
    
#### End of Fruityvice section

# streamlit.stop()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)



