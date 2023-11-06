import os

import streamlit as st
from st_aggrid import AgGrid
from streamlit_extras.add_vertical_space import add_vertical_space
from DButil import *
from streamlit_autorefresh import st_autorefresh
import datetime
import pytz

@st.cache_data
def convert_df(data):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return data.to_csv().encode('utf-8')


def get_df():
    return (get_dataframe(cs_tables["AP"], os.environ["dpmo_ws_bkc_no"]),
            get_dataframe(cs_tables["SP"], os.environ["dpmo_server_bkc_no"]),
            get_dataframe(cs_tables["EMR_FSP_API"], os.environ["dpmo_fsp_bkc_no"]))


def show_df(cs_frame, key):
    left, center, right = st.columns([3, 3, 0.74])
    with center.container():
        add_vertical_space(5)
        st.download_button(
            label="Download data as CSV",
            data=convert_df(cs_frame),
            file_name='cycling_status.csv',
            mime='text/csv',
            key='cs_dl'+key
        )


def main():
    st.session_state.token = [os.environ['dpmo_streamlit_token']]

    st.set_page_config(
        page_title="DPMO Status Collector",
        page_icon="♾️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st_autorefresh(interval=120000, key="pageautorefresh")
    st.markdown("<h2 style='text-align: center; color: blue; font-weight: bold;'>DPMO Cycling Status Collector</h2>",
                unsafe_allow_html=True)
    st.markdown('<style>div.block-container{padding-top:4rem;}</style>', unsafe_allow_html=True)
    IST = pytz.timezone('Asia/Kolkata')
    st.info('Data is last refreshed at: {} (IST)'.format(datetime.datetime.now(IST).strftime("%d-%m-%Y, %H:%M:%S")))
    st.success('This page shows only the current state of system(s), older data can be seen in historical data')

    ap_df, sp_df, fsp_df = get_df()

    tab1, tab2, tab3 = st.tabs(["EMR-Server", "EMR-Workstation", "EMR-FSP-API"])
    grid_options = {
        'defaultColDef': {'minWidth': 5, 'editable': False, 'filter': True, 'resizable': True, 'sortable': True},
        'columnDefs': [
            {'headerName': 'ID', 'valueGetter': 'node.id', "width": 70},
            {'headerName': 'System', 'field': 'System'},
            {'headerName': "HW Status",
             "marryChildren": True,
             'children': [
                 {"field": "QDF", "columnGroupShow": "open"},
                 {"field": "Sockets", "columnGroupShow": "open"},
                 {"field": "OS", "columnGroupShow": "open"},
                 {"field": "HW CFG Description", "columnGroupShow": "open"},
                 {"field": "IFWI", 'width': 140}]},
            {'headerName': "DPMO Status",
             "marryChildren": True,
             "children": [
                 {'headerName': 'Cycling Type', 'field': 'Cycling Type', 'type': [], 'width': 140},
                 {'headerName': 'Cycling Start Date', 'field': 'Cycling Start Date', 'type': [],
                  "columnGroupShow": "open", "filter": 'agDateColumnFilter'},
                 {'headerName': 'Cycling Stop Date', 'field': 'Cycling Stop Date',
                  'type': [], "columnGroupShow": "open", "filter": 'agDateColumnFilter'},
                 {'headerName': 'Target Cycles', 'field': 'Target Cycles',
                  'type': ['numericColumn', 'numberColumnFilter'], "columnGroupShow": "open"},
                 {'headerName': 'BKC', 'field': 'BKC', 'type': [], 'width': 100},
                 {'headerName': 'Attempt', 'field': 'Attempt', 'type': [],'width': 120},
                 {'headerName': 'Cycles Run', 'field': 'Cycles Run',
                  'type': ['numericColumn', 'numberColumnFilter'], 'width': 150},
                 {'headerName': 'Nof Failures', 'field': 'Nof Failures',
                  'type': ['numericColumn', 'numberColumnFilter'], "columnGroupShow": "open"},
                 {'headerName': 'Failure Description', 'field': 'Failure Description',
                  'editable': True, "columnGroupShow": "open", "width": 600},
                 {'headerName': 'PostCode', 'field': 'PostCode', 'type': [], "columnGroupShow": "open"},
                 {'headerName': 'Current State', 'field': 'Current State', 'type': [], 'width': 150},
             ]
             },
            {'headerName': 'Log Path', 'field': 'Log Path', 'type': [], 'width':540},
            {'headerName': 'PCIe Info', 'field': 'PCIe Info', 'type': []},
            {'headerName': 'Comment', 'field': 'Comment', 'type': [], 'editable': True}
        ]}
    with tab1:
        grid_return = AgGrid(sp_df, gridOptions=grid_options, theme="alpine", key="cs_sp")
        sp_cs_frame = grid_return['data']
        show_df(sp_cs_frame, "SP")

    with tab2:
        grid_return = AgGrid(ap_df, gridOptions=grid_options, theme="alpine", key="cs_ap")
        ap_cs_frame = grid_return['data']
        show_df(ap_cs_frame, "AP")

    with tab3:
        grid_return = AgGrid(fsp_df, gridOptions=grid_options, theme="alpine", key="cs_fsp")
        fsp_cs_frame = grid_return['data']
        show_df(fsp_cs_frame, "fsp")


if __name__ == "__main__":
    main()
