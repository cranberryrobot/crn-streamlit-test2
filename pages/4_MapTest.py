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




def barchart():
    @st.experimental_memo
    def from_data_file():

        url = ("https://data.police.uk/api/crimes-street/all-crime?lat=52.629729&lng=-1.131592&date=2023-01")
        data = pd.read_json(url)
        df = pd.DataFrame(data)
        data = df.join(pd.json_normalize(df.location)).drop(columns=['location'])

        return data

    chart_data = pd.DataFrame(from_data_file())
    st.write(chart_data)

    # st.bar_chart(chart_data, x='location_type', y='count()')

    chart = alt.Chart(chart_data).mark_bar().encode(
        x='location_type',
        y='count()',
    )

    st.altair_chart(chart)

st.set_page_config(page_title="Bar Chart Test", page_icon="📈")
st.markdown("# Bar Chart Test")
st.sidebar.header("Bar Charts")

barchart()