import streamlit as st
import pickle
import pandas as pd
import requests

anime_list=pickle.load(open("anime.pkl","rb"))
similar=pickle.load(open("similar.pkl","rb"))

anime_lists=anime_list['name']

def fetch_poster(anime_id):
    response= requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}/pictures')
    data=response.json();
    return data['data'][0]["jpg"]["image_url"]

def recommend(anime):
     anime_ind=anime_list[anime_list['name']==anime].index[0]
     dist=similar[anime_ind]
     anime_l=sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:6]
     recommended_anime=[]
     recommended_anime_poster=[]
     for i in anime_l:
        
        recommended_anime.append(anime_list.iloc[i[0]]['name'])
        recommended_anime_poster.append(fetch_poster(anime_list.iloc[i[0]]['anime_id']))
     return recommended_anime,recommended_anime_poster

st.title("Anime Recommendation Model")
selected_anime= st.selectbox(
    'Search You Anime Here',
    anime_lists)


if st.button('Recommend Anime'):
   names, posters= recommend(selected_anime)

   st.title(f'5 animes related to {selected_anime} are:')
   i=0
   for image_url in posters:
      st.markdown(f'<h3 style="text-align: center;">{names[i]}</h3>', unsafe_allow_html=True)
    #  image_style = "display: block; margin: 0 auto;"
    #   st.image(posters[i], width=300)
      st.markdown(f'<image style="width: 100%; height: 400px; object-fit: contain;  margin: auto; margin-bottom: 20px;" src="{posters[i]}" />', unsafe_allow_html=True)
      
      i=i+1