# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from urllib.error import URLError

import pandas as pd
import pydeck as pdk

import streamlit as st
from streamlit.hello.utils import show_code
from flatten_json import flatten
import altair as alt




def barchart(long=52.62, lat=-1.32):
    @st.experimental_memo
    def from_data_file():

        url = (f"https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={long}")
        try:
            data = pd.read_json(url)
            df = data
            #pd.DataFrame(data)
            #df['police_force_api_url'] = df.agg(lambda x: f"https://data.police.uk/api/locate-neighbourhood?q={x['latitude']},{x['longitude']}", axis=1)
            st.write(df.columns.tolist())
            # df['police_force'] = df.apply(lambda x: pd.read_json(x['police_force_api_url']), axis=1, index=[0])
            return df
        except Error:
            st.error("The data with the longitudes and lattitudes indicated could not be found, or an error occurred.")

    chart_data = pd.DataFrame(from_data_file())
    st.write(chart_data)

    # st.bar_chart(chart_data, x='location_type', y='count()')

    chart = alt.Chart(chart_data).mark_bar().encode(
        x='location_type',
        y='count()',
    )

    st.altair_chart(chart)

st.set_page_config(page_title="Bar Chart Test", page_icon="📊")
st.markdown("# Bar Chart Test")
st.sidebar.header("Bar Charts")

with st.form("Location_Form"):
   form_long = st.number_input("longtude")
   form_lat = st.number_input("latitude")

   submitted = st.form_submit_button("Submit")
   if submitted:
       barchart(lat=form_lat, long=form_long)

