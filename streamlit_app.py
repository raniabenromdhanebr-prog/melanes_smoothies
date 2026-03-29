# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests  
# Write directly to the app.
st.title("customize your smoothie!")
st.write(
  "chooose your smooth")
#option=st.selectbox('what is your favourite?',
      #            ( 'Banana','Straw','Peaches'))
#st.write('your favorites is',option)
name=st.text_input('name on the smooth')
st.write('the name on your smooth will be ', name)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
list =st.multiselect('Choose up to 5 ingred'
                     ,my_dataframe 
                    , max_selections=5)

if list :
  #  st.write(list)
  #  st.text(list)
    ingredients_string=''

    for fruit_chosen in list :
        ingredients_string+=fruit_chosen+' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """',
                     '"""+name+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit')
    if time_to_insert:
         session.sql(my_insert_stmt).collect()
         st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json(),use_container_width=true)
