from urllib.error import URLError

import pandas as pd
import pydeck as pdk

import streamlit as st
from streamlit.hello.utils import show_code

import altair as alt
from streamlit_extras.grid import grid as st_grid, grid
import numpy as np

alt.renderers.set_embed_options(
    padding={"left": 0, "right": 0, "bottom": 0, "top": 0}
)



def get_party_colour(partyname, inversebool:bool):

    partyname = partyname.strip()
    partyname = partyname.upper()

    if inversebool:
        if partyname == "LAB":
            return "black"
        elif partyname == "LD":
            return "black"
        elif partyname == "TUSC":
            return "black"
        elif partyname == "IND":
            return "black"
        else:
            return "white"
    else:
        if partyname == "CON":
            return "blue"
        elif partyname == "LAB":
            return "red"
        elif partyname == "GREEN":
            return "green"
        elif partyname == "LD":
            return "orange"
        elif partyname == "TUSC":
            return "lightred"
        elif partyname == "IND":
            return "pink"
        elif partyname == "YORKS":
            return "lightblue"
        else:
            return "grey"

@st.cache_data(experimental_allow_widgets=True)
def election_data():
    df = pd.read_excel('pages/LEC.xlsx', index_col=0)
    ward_list = df.drop_duplicates("WARDNAME")
    district_list = df.drop_duplicates("DISTRICTNAME")
    #st.dataframe(ward_list)
    district_list = district_list[["DISTRICTNAME"]]
    #ward_list = ward_list['ward_district_name'] = ward_list.agg(lambda x: f"{x['WARDNAME']} ({x['DISTRICTNAME']})", axis=1)
    selected_district = st.selectbox("Council area", district_list, index=None, placeholder="Search for a council area...")
    
    if selected_district == None:
        ward_list = ward_list[["WARDNAME"]]
    else:
        ward_list = ward_list[ward_list.DISTRICTNAME==selected_district]
        ward_list = ward_list[["WARDNAME"]]
    
    selected_ward = st.selectbox("Ward", ward_list, index=None, placeholder="Search for a ward or division...")

    #ward_list = ward_list[["DISTRICTNAME"]=selected_district]


    
    if selected_ward == None:
        st.error("No ward selected")
    else:
        ward_result = df[df.WARDNAME==selected_ward]
        range_ = ['green', 'lightgrey']
        turnout_amt = float(ward_result[["TURNOUT"]].head(1).to_string(header=None, index=None))
        turnout = pd.DataFrame(columns=["turnout"], data=[[turnout_amt], [100-turnout_amt]])
    
        c1 = alt.Chart(turnout).mark_arc(
                radius=30,
                radius2=50,
                theta=0,
                theta2=2,
                cornerRadius=0,
                padAngle=0,
            ).encode(
                theta=alt.Theta("turnout:Q"),
                color=alt.Color("turnout:N", scale=alt.Scale(range=range_)).legend(None),
                tooltip=alt.value(None)
            ).properties(
                height=70
            )
        
        col1, col2 = st.columns([0.15, 0.85])

        with col1:
            st.altair_chart(c1, theme=None, use_container_width=True)
        
        with col2:
            st.metric("Turnout", turnout_amt)


        ward_table = ward_result[["PARTYNAME","NAME", "VOTE"]]

        ward_table['party_colour'] = ward_table.agg(lambda x: get_party_colour(x['PARTYNAME'], False), axis=1)
        ward_table['party_colour_inverse'] = ward_table.agg(lambda x: get_party_colour(x['PARTYNAME'], True), axis=1)
        ward_table['html_table_code'] = ward_table.agg(lambda x: f"<tr><td style='background-color: {x['party_colour']}; font-weight: bold; color: {x['party_colour_inverse']};'>{x['PARTYNAME']}</td><td style='width:600px;'>{x['NAME']}</td><td>{x['VOTE']}</td></tr>", axis=1)


        html_table = ward_table['html_table_code'].to_list()
        html_table = "".join(str(h) for h in html_table)

        st.markdown(html_table, unsafe_allow_html=True)


        
        #st.dataframe(df)


st.set_page_config(page_title="Election", page_icon="🗳️")
st.markdown("# Election Test")
st.sidebar.header("Election")

election_data()