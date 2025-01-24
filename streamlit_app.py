# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":mango::strawberry: Customize your smoothie :strawberry::mango:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """)

name_order = st.text_input("Name on the smoothie")
st.write("The name on your smoothie will be ", name_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect("Choose up to 5 ingredients : ", my_dataframe, max_selections=5)

if ingredient_list:
    ingredients_string = ""

    for fruit_choosen in ingredient_list:
        ingredients_string += fruit_choosen + " "

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+ name_order +"""')"""

    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_order, icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response)
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
