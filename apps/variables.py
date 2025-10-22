import streamlit as st
import geopandas as gpd
import datetime

# import farms vector file as a gdf

def get_farms_gdf():
    farms_gdf = gpd.read_file(r"data/vector/ce_farms.gpkg")
    farms_gdf = farms_gdf[['farmer', 'crop', 'district', 'province', 'area_ha', 'geometry']]
    return farms_gdf


def get_sh_farms():
    gdf = gpd.read_file(r"data/vector/field_measure_farms.gpkg")
    # gdf = gdf[:500]
    # gdf = gdf[['farmer_id', 'camp', 'pea', 'hub', 'fs', 'district', 'region','geometry']]
    gdf['lon'] = gdf.geometry.x
    gdf['lat'] = gdf.geometry.y

    return gdf

def available_crop_health_metrics():
    health_metrics = ['Crop Health', 'Crop Moisture', ]
    return health_metrics

def farm_names_list():
    farms_gdf = get_farms_gdf()
    # List of farms
    farm_names = sorted(list(set(farms_gdf["farmer"].to_list())))
    return farm_names

def add_selectors_crop_health(backtrack_days=7):
    farm_names = farm_names_list()

    # crop health metrics
    indices_list = available_crop_health_metrics()

    # specify columns and their widths
    farm_names_col, indices_list_col, start_date_col, end_date_col, max_cloud_cover_col = st.columns([3, 3, 2, 2, 3])

    with farm_names_col:
        selected_farm_name = st.selectbox(
            "Select the farm to monitor",
            farm_names,
            index=None,
            placeholder="Select farm...",
            key=1
        )

    with indices_list_col:
        selected_index = st.selectbox(
            "Select the metric to monitor",
            indices_list,
            index=None,
            placeholder="Select metric...",
            key=2
        )

    with start_date_col:
        selected_start_date = str(st.date_input(
            "Select start date",
            datetime.date.today() - datetime.timedelta(days=backtrack_days),
            key=3
        ))

    with end_date_col:
        selected_end_date = str(st.date_input(
            "Select end date",
            datetime.date.today(),
            key=4
        ))

    with max_cloud_cover_col:
        # max_cloud_cover = st.text_input('Select maximum cloud cover',
                                    # 0, 100, 20, step=5)
        max_cloud_cover = st.slider(
            'Select maximum cloud cover',
            min_value =0,
            max_value=100, 
            value= 20,
            step=5,
            key=5
            )

    return selected_farm_name, selected_index, selected_start_date, selected_end_date, max_cloud_cover

def add_selectors_crop_monitor(backtrack_days=7):
    farm_names = farm_names_list()

    # crop health metrics
    indices_list = available_crop_health_metrics()

    # specify columns and their widths
    farm_names_col, indices_list_col, start_date_col, end_date_col, max_cloud_cover_col = st.columns([3, 3, 2, 2, 3])

    with farm_names_col:
        selected_farm_name = st.selectbox(
            "Select the farm to monitor",
            farm_names,
            index=None,
            placeholder="Select farm...",
            key=10
        )

    with indices_list_col:
        selected_index = st.selectbox(
            "Select the metric to monitor",
            indices_list,
            index=None,
            placeholder="Select metric...",
            key=11
        )

    with start_date_col:
        selected_start_date = str(st.date_input(
            "Select start date",
            datetime.date.today() - datetime.timedelta(days=backtrack_days),
            key=12
        ))

    with end_date_col:
        selected_end_date = str(st.date_input(
            "Select end date",
            datetime.date.today(),
            key=13
        ))

    with max_cloud_cover_col:
        # max_cloud_cover = st.text_input('Select maximum cloud cover',
                                    # 0, 100, 20, step=5)
        max_cloud_cover = st.slider(
            'Select maximum cloud cover',
            0, 100, 20, step=5,
            key=14
            )

    return selected_farm_name, selected_index, selected_start_date, selected_end_date, max_cloud_cover
