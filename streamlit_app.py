import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
def get_fruityvice_data(fruit_choice):
  #normalize json
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
def get_fruit_load_list():

  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    my_data_rows = my_cur.fetchall()
    return my_data_rows
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    #my_cur.execute("insert into fruit_load_list values('{}')".format(new_fruit))
    my_cur.execute("insert into fruit_load_list values('test')")
    
    return 'Thanks for adding ' + new_fruit

  
  
  
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Bolied Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
#New section
streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
  else: 
      #streamlit.write('The user entered ', fruit_choice)
      #import requests
      #make sure this streamlit.dataframe is at end
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()


streamlit.header("The fruit load list contains:")
#Add button to load fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  my_cnx.close()

add_my_fruit = streamlit.text_input("What fruit you would like to add?")
if streamlit.button('Add Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
  my_cnx.close()

streamlit.stop()# to prevent running lower codeafter this point

