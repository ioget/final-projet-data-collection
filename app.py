import streamlit as st
import pandas as pd
from scraper import *
import numpy as np
import re

import streamlit as st
import pydeck as pdk
import pandas as pd

import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

from database import insert_if_not_exists,load_data_from_database, get_count_by_category,get_dogs,get_sheep,get_poultry_rabbit, get_other_animals,get_count_by_type_df, get_count_by_location_df
from geo import geocode_location,geo_map



#################################################


def show_location_pie_chart():
    df = get_count_by_location_df()

    theme = st.get_option("theme.base")

    if theme == "dark":
        bg = "#0e1117"
        text_color = "white"
    else:
        bg = "white"
        text_color = "black"

    fig, ax = plt.subplots(figsize=(6, 7.25),facecolor="#292a2e")
    ax.set_facecolor(bg)

    ax.pie(
        df["total"],
        labels=df["location"],
        autopct="%1.1f%%",
        startangle=90,
        textprops={"color": 'white'}
    )

    ax.axis("equal")
    st.pyplot(fig)





def show_category_cards():
    counts = get_count_by_category()

    if not counts:
        st.info("No data found in database.")
        return

    # image_map = {
    #     "dog": "image/dog.jpeg",
    #     "sheep": "image/mouton.jpeg",
    #     "poultry-rabbit": "image/poule.jpeg",
    #     "other": "image/other.jpeg",
    # }
    
    image_map = {
    "dog": {"path": "image/dog-removebg-preview.png", "width": 150},
    "sheep": {"path": "image/mouton-removebg-preview.png", "width": 210},
    "poultry-rabbit": {"path": "image/poule-removebg-preview.png", "width": 133},
    "other": {"path": "image/other-removebg-preview.png", "width": 205},
}

    cols = st.columns(len(counts))

    for i, (category, count) in enumerate(counts.items()):
        with cols[i]:
            left, mid, right = st.columns([1, 2, 1])
            with mid:
                st.image(image_map.get(category, image_map["other"])['path'], width=image_map.get(category, image_map["other"])["width"])
                st.write(category.capitalize())
                st.write(f"**{count}** animals")



def scrape_clean_mode():
    st.write("Hello choose you animal category to scrape")
        

    urls = {
        "Dogs": "https://sn.coinafrique.com/categorie/chiens",
        "Sheep": "https://sn.coinafrique.com/categorie/moutons",
        "Poultry & Rabbits": "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons",
        "Other Animals": "https://sn.coinafrique.com/categorie/autres-animaux"
    }

    if "selected_url" not in st.session_state:
        st.session_state.selected_url = urls["Dogs"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("image/dog.jpeg", width=150)
        if st.button("Dogs"):
            st.session_state.selected_url = urls["Dogs"]

    with col2:
        st.image("image/mouton.jpeg", width=210)
        if st.button("Sheep"):
            st.session_state.selected_url = urls["Sheep"]

    with col3:
        st.image("image/poule.jpeg", width=133)
        if st.button("Poultry & Rabbits"):
            st.session_state.selected_url = urls["Poultry & Rabbits"]

    with col4:
        st.image("image/other.jpeg", width=205)
        if st.button("Other Animals"):
            st.session_state.selected_url = urls["Other Animals"]



    base_url = st.session_state.selected_url
    
    
    site = st.session_state.selected_url.split('/')[-1]
    st.markdown(f"Great you choose **{site}** click and scrape now!!")

    st.text_input("Website URL", base_url, disabled=True)
    


    page_start = st.number_input("Start Page", min_value=1, value=1)
    page_end = st.number_input("End Page", min_value=1, value=2)

    if st.button("Start Scraping"):
        with st.spinner("Scraping..."):
            st.session_state.db_inserted = False
            
            data = extract_website_items(base_url, page_start, page_end)
            st.success(f"{len(data)} items collected")
            
            if(len(data) == 0):
                st.warning("No data scraped. Please check different page range.")
                return
            
            df = pd.DataFrame(data)
            
            df.drop_duplicates(inplace=True)

            df["price"] = df["price"].replace("Prix sur demande", np.nan)
            df["price_clean"] = df["price"].apply(
                lambda x: int(re.sub(r"[^\d]", "", str(x))) if pd.notna(x) else np.nan
            )
            median_price = df["price_clean"].median()
            df["price"] = df["price_clean"].fillna(median_price)
            df.drop(columns=["price_clean"], inplace=True)

            #  Sauver DF dans la session
            st.session_state.df_clean = df

    if "df_clean" in st.session_state:
        df = st.session_state.df_clean

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        colA, colB = st.columns(2)

        with colA:
            st.download_button(
                "⬇️ Download CSV",
                csv,
                "coinafrique_dogs.csv",
                "text/csv"
            )

        if "db_inserted" not in st.session_state:
            st.session_state.db_inserted = False

        with colB:
            if st.button("🔵 Insert in Database", disabled=st.session_state.db_inserted):
                st.session_state.db_inserted = True
                
                total_inserted = 0  # Track total insertions
                
                for _, item in df.iterrows():
                    type_map = {
                        "chiens": "dog",
                        "moutons": "sheep",
                        "poules-lapins-et-pigeons": "poultry-rabbit",
                    }

                    _type = type_map.get(site, "other")
                    
                    result = insert_if_not_exists(
                        item["name"],
                        str(item["price"]),
                        item["location"],
                        item["url_image"],
                        _type
                    )
                    
                    total_inserted += result[1]  # Accumulate the count
                
                # Display results after the loop
                st.write(f"✅ Number of new records inserted: {total_inserted}")
                if total_inserted > 0:
                    st.toast("Data inserted successfully!")
                else:
                    st.toast("No new data to insert (all records already exist).")
                    

def show_csv_tables_buttons():

    files = {
        "Dogs": "data/chien-coinafrique-chien.csv",
        "Sheep": "data/chien-coinafrique-mouton.csv",
        "Rabbits": "data/chien-coinafrique-lapins.csv",
        "Other": "data/chien-coinafrique-autre.csv",
    }

    if "selected_csv" not in st.session_state:
        st.session_state.selected_csv = None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("image/dog-removebg-preview.png", width=150)
        if st.button("Show Dogs"):
            st.session_state.selected_csv = files["Dogs"]

    with col2:
        st.image("image/mouton-removebg-preview.png", width=210)
        
        if st.button("Show Sheep"):
            st.session_state.selected_csv = files["Sheep"]

    with col3:
        st.image("image/poule-removebg-preview.png", width=133)
        
        if st.button("Show Rabbits"):
            st.session_state.selected_csv = files["Rabbits"]

    with col4:
        st.image("image/other-removebg-preview.png", width=205)
        
        if st.button("Show Other"):
            st.session_state.selected_csv = files["Other"]

    if st.session_state.selected_csv:
        df = pd.read_csv(st.session_state.selected_csv)
        st.dataframe(df)



      
    
 


def scrape_withoutclean_mode():
        st.write("Hello choisse ")
        show_csv_tables_buttons()
        


################################################






st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

st.sidebar.title("Menu")

if st.sidebar.button("Dashboard"):
    st.session_state.page = "Dashboard"
   
if st.sidebar.button("Scrape Data"):
    st.session_state.page = "Scrape Data"



if st.sidebar.button("Evaluation Form"):
    st.session_state.page = "Evaluation Form"



######################### session ######################################


if st.session_state.page == "Dashboard":
    st.title("Dashboard")
    # print("Dashboard")
    
     
    if st.session_state.page == "Dashboard":
        
        st.subheader("Data Visualization")
        
        show_category_cards()
        

        df = load_data_from_database()

        if df.empty:
            st.warning("⚠️ No data found in database.")
        else:

            col1, col2 = st.columns(2)

            #  HISTOGRAMME DES PRIX
            with col1:
                # st.subheader(" Distribution of Price")

                df["price"] = df["price"].apply(
                    lambda x: int(re.sub(r"[^\d]", "", str(x))) if pd.notna(x) and "Prix" not in str(x) else np.nan)

                median_price = df["price"].median()

                df["price"] = df["price"].fillna(median_price)

                hist_values, bin_edges = np.histogram(df["price"], bins=20)

                chart_df = pd.DataFrame({
                    "Price Range": bin_edges[:-1],
                    "Count": hist_values
                })

                chart_df = chart_df.set_index("Price Range")
                # st.bar_chart(chart_df)
                st.subheader("Top 10 Heat Location Ranking")
                
                
                show_location_pie_chart()

            with col2:
                st.subheader(" Information localisation")

               

                df["lat"] = df["location"].map(lambda x: geo_map.get(x, (None, None))[0])
                df["lon"] = df["location"].map(lambda x: geo_map.get(x, (None, None))[1])
                
                # df["lat"], df["lon"] = zip(*df["location"].apply(geocode_location))
                
                df_map = df.dropna(subset=["lat", "lon"])


                df_map = df.dropna(subset=["lat", "lon"])

                if df_map.empty:
                    st.warning(" No location data available for the map.")
                else:
                    layer = pdk.Layer(
                        "ScatterplotLayer",
                        data=df_map,
                        
                        get_position="[lon, lat]",
                        get_radius=12000,
                        get_fill_color=[0, 0, 255, 180],
                        pickable=True,                       
               
              
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
               
                extruded=True,
                    )

                    view_state = pdk.ViewState(
                        # latitude=14.4974,
                        # longitude=-14.4524,
                        latitude=14.7167,
                        longitude=-17.4677,
                        zoom=10.5,
                        pitch=50,
                      
                    )

                    deck = pdk.Deck(layers=[ pdk.Layer(
                "HexagonLayer",
                data=df_map,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=10,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=df_map,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),], initial_view_state=view_state)
                    st.pydeck_chart(deck)
        
        
        st.subheader(" Animal Category Distribution")

        df_c = get_count_by_type_df()
        df_c = df_c.set_index("_type")
        st.bar_chart(df_c)



        tab_dog, tab_sheep, tab_poultry, tab_other = st.tabs(
            ["Dogs", "Sheep", "Poultry & Rabbit", "Other"]
        )
        

        with tab_dog:
            df = get_dogs()
            st.dataframe(df)

        with tab_sheep:
            df = get_sheep()
            st.dataframe(df)

        with tab_poultry:
            df = get_poultry_rabbit()
            st.dataframe(df)

        with tab_other:
            df = get_other_animals()
            st.dataframe(df)
            
       





elif st.session_state.page == "Scrape Data":
    
    
    st.title("Scrape Data")

  

    if "scrape_mode" not in st.session_state:
        st.session_state.scrape_mode = None

    tab_clean, tab_raw = st.tabs(["Scrape and Clean", "Scrape Without Clean"])

 
    with tab_clean:
        
        scrape_clean_mode()
       
       

    with tab_raw:
       
        scrape_withoutclean_mode()


  

    # if st.session_state.scrape_mode in actions:
    #     actions[st.session_state.scrape_mode]()



elif st.session_state.page == "Evaluation Form":
    st.title("Evaluation Forms")
    st.write("Please fill one of the forms below to evaluate this app")

    # Création des deux onglets
    tab1, tab2, tab3 = st.tabs(["KoBo Form", "Google Form", 'App Tutorial'])

    with tab1:
        st.subheader("Evaluation via KoBoToolbox")
        components.iframe(
            "https://ee.kobotoolbox.org/x/ZbJopiyf",
            height=900,
            scrolling=True
        )

    with tab2:
        st.subheader("Evaluation via Google Form")
        components.iframe(
            "https://docs.google.com/forms/d/e/1FAIpQLSeDxrGjUnl9Rh1TQdeWTbxyzQJ6RYjW87cgC9u25Dzx4_Nfug/viewform",
            height=900,
            scrolling=True
        )
        
    with tab3:
        st.subheader("App Tutorial")
        
        st.video("https://drive.google.com/file/d/104Z-Ju8b4LDPnjMkUQRfuY97fIR7PAsG/view?usp=drive_link")
    crolling=True
        
        
        
st.markdown("---")
st.caption("Made by Dev ❤️  Rosly MAMEKEM")
