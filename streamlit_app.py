
import streamlit as st
import json, requests, pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from ingredient_parser import ingredient_parser
import config, rec_sys
import time

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://github.com/celiaXH/demoapp/blob/main/background_img.jpg?raw=true");
background-size: 90%;
background-position: top left;
background-repeat: repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title('What can we cook !?')
st.markdown("**It's been a daily question for everyone coming back home and looking at the fridge, hardly trying to bring up an idea for evening dinner.**")
st.write("**With given a list of ingredients left in your fridge, this recipe recommender system will provide 5 most matching recipes from allrecipe.com**")
st.subheader("What's in your fridge?")
ingredients = st.text_input(
        "Enter food ingredients (seperate ingredients with a comma)",
        "onion, chorizo, chicken thighs",
    )

start_execution = st.button('Give me recommendation!')
if start_execution:
    gif_runner = st.image("input/cooking_gif.gif")
    recipe = rec_sys.RecSys(ingredients)
    response = {}
    count = 1
        
    for index, row in recipe.iterrows():
        response[count] = {
            'Recipe': str(row['recipe']),
            'Score': str(row['score']),
            'Ingredients': str(row['ingredients']),
            'url': str(row['url'])
        }
        count += 1
    df= pd.DataFrame(response).T

    def make_clickable(url, name):
        return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

    df['Recipe link'] = df.apply(lambda x: make_clickable(x['url'], x['Recipe']), axis=1)
    df2= df[["Recipe link","Score","Ingredients"]]
    gif_runner.empty()
    st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
    
# sidebar stuff
with st.sidebar.expander("How it works?", expanded=True):
    st.markdown("## How it works? :thought_balloon:")
    st.markdown(
        f"1. Web Scraping recipes Data via Beautiful Soup"
    )
    st.markdown(
        f"2. Building a Recipe Recommendation system using Scikit-Learn, NLTK, Word2Vec"
    )
    st.markdown(
        f"3. depolyment with Streamlit"
    )

    st.markdown("[![Foo]()](https://github.com/celiaXH/demoapp)")



