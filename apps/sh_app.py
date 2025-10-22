import streamlit as st
import folium
from folium.plugins import MarkerCluster, MeasureControl
import xyzservices.providers as xyz
from streamlit_folium import folium_static
from apps import sh_functions, variables

st.set_page_config(layout="wide")

gdf = variables.get_sh_farms()

rename_color_by = {'Region': 'region_id', 'District': 'district_id', 'Hub': 'hub_id',
                   'Camp': 'camp_id', 'FS': 'fs_id', 'PEA': 'pea_id'}

def app():
    st.header("Field Locations")

    with st.expander("Click to filter map and metrics"):
        selected_region, selected_district, selected_hub, selected_camp = sh_functions.add_sh_location_filter_selectboxes(gdf)
        selected_fs, selected_pea, selected_farmer_id = sh_functions.add_sh_personnel_filter_selectboxes(gdf)

    filtered_gdf = sh_functions.get_filtered_gdf(
        gdf, selected_region, selected_district, selected_hub, selected_camp, 
        selected_fs, selected_pea, selected_farmer_id
        )

    view_cluster_col, color_by_col = st.columns([3,3])
    with view_cluster_col:
        view_cluster = st.checkbox("View fields as clusters", value=True, key=41)

    if not view_cluster:
        with color_by_col:
            selected_color_by = st.radio(
                "Color fields by...", rename_color_by.keys(), index=0, key=42, horizontal=True
            )

        gotten_colors = sh_functions.get_colors(selected_color_by, filtered_gdf)

    else:
        selected_color_by="None"
        gotten_colors = None

    with st.expander("Click to view metrics"):
        sh_functions.get_scorecards(filtered_gdf)

        # view_graph = st.checkbox("View graph", value=False, key=40)
        with st.expander("View chart"):
            sh_functions.get_altair_chart(filtered_gdf, selected_color_by, gotten_colors)

    m = folium.Map(tiles="CartoDB dark_matter", control_scale=True,
                   draw_control=False, layer_control=False)
    
    folium.TileLayer(
        tiles=xyz.Esri.WorldImagery.build_url(),
        name="Esri WorldImagery",
        attr=xyz.Esri.WorldImagery.attribution,  # ✅ required
        overlay=False,
        control=True,
        show=False
    ).add_to(m)
            
    m.add_child(MeasureControl(
        primary_length_unit='kilometers',
        secondary_length_unit='meters',
        primary_area_unit='sqmeters',
        secondary_area_unit='hectares'
    ))

    # Get bounds: [minx, miny, maxx, maxy]
    minx, miny, maxx, maxy = filtered_gdf.total_bounds

    # Fit map to bounds
    m.fit_bounds([[miny, minx], [maxy, maxx]])

    # Create a FeatureGroup named "Farms"
    farms_group = folium.FeatureGroup(name="Farms")

    if view_cluster:
        # Add marker cluster to the feature group
        marker_cluster = MarkerCluster().add_to(farms_group)
    else:
        marker_cluster = m

    with st.spinner("Patience makes the crop work...", show_time=True):
        sh_functions.add_map_cicle_markers(
            filtered_gdf, gotten_colors, selected_color_by, rename_color_by, marker_cluster
            )

        # Add the feature group (with clustered points) to the map
        farms_group.add_to(m)

        # Add layer control
        folium.LayerControl(collapsed=True).add_to(m)
        
        folium_static(m, width=None)

    disclaimer_col, data_source_col = st.columns([6,2])
    with disclaimer_col:
        st.write("Disclaimer: *Not all fields locations are available*")
    with data_source_col:
        st.write("Data Source: *Field measures survey*")
