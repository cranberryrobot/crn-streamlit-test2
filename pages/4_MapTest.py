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




def mapping_demo():
    @st.cache_data
    def from_data_file():
        url = (
            "https://data.police.uk/api/crimes-street/all-crime?lat=52.629729&lng=-1.131592&date=2023-01"
        )

        data = pd.read_json(url)

        flattened_data = [flatten(d) for d in data]

        data = pd.DataFrame(flattened_data)

        st.write(data)
        return data

    try:
        ALL_LAYERS = {
            "Police Data Points": pdk.Layer(
                "HexagonLayer",
                data=from_data_file(),
                get_position=['location_lattitude', 'location_longitude'],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            )
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style=None,
                    initial_view_state={
                        "latitude": 55.37,
                        "longitude": 3.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="Test", page_icon="🌍")
st.title("This is a title")
st.write(
    """This is some text"""
)

mapping_demo()

