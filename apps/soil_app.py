import streamlit as st
import geemap.foliumap as geemap_folium
from folium.plugins import MeasureControl
import geopandas as gpd
from apps import soil_functions, ee_functions


aoi_gdf = gpd.read_file(r"data/vector/zambia_aoi.gpkg")
texture_classes = ['Clay', 'Sandy Clay', 'Clay Loam',
                    'Sandy Clay Loam', 'Sandy Loam', 'Loamy Sand','Sand']

def app():
    soil_tab, = st.tabs(['Soil Suitability'])

    with soil_tab:
        st.header("Analyse Soil Suitability")

        toggle = st.toggle(" Activate overlay analysis")

        col1, col2, col3, col4, col5 = st.columns(5)

        options = soil_functions.get_soil_dataset(None)
        selected_dataset_names_list = []
        selected_datasets = {}
        with col1:
            dataset1_name = st.selectbox(
                "Select dataset",
                options=options,
                index = None,
                placeholder="Select dataset",
                key=60
            )

        if toggle:
            if dataset1_name in options:
                options.remove(dataset1_name)
                selected_dataset_names_list.append(dataset1_name)

            with col2:
                dataset2_name = st.selectbox(
                    "Select dataset 2",
                    options=options,
                    index = None,
                    placeholder="Select dataset",
                    key=61
                )

            if dataset2_name:
                if dataset2_name in options:
                    options.remove(dataset2_name)
                    selected_dataset_names_list.append(dataset2_name)

                with col3:
                    dataset3_name = st.selectbox(
                        "Select dataset 3",
                        options=options,
                        index = None,
                        placeholder="Select dataset",
                        key=62
                    )

            if dataset2_name and dataset3_name:
                if dataset3_name in options:
                    options.remove(dataset3_name)
                    selected_dataset_names_list.append(dataset3_name)
                with col4:
                    dataset4_name = st.selectbox(
                        "Select dataset 4",
                        options=options,
                        index = None,
                        placeholder="Select dataset",
                        key=63
                    )

            if dataset2_name and dataset3_name and dataset4_name:
                if dataset4_name in options:
                    options.remove(dataset4_name)
                    selected_dataset_names_list.append(dataset1_name)
                with col5:
                    dataset5_name = st.selectbox(
                        "Select dataset 5",
                        options=options,
                        index = None,
                        placeholder="Select dataset",
                        key=64
                    )
                if dataset2_name and dataset3_name and dataset4_name:
                    selected_dataset_names_list.append(dataset5_name)


            # Add container to filter datasets
            with st.expander("Click to filter selected datasets"):
                col1b, col2b, col3b, col4b, col5b = st.columns(5)

                with col1b:
                    if dataset1_name == 'Texture Class':
                        dataset1_range = st.multiselect(
                            f"Filter {dataset1_name}",
                            default=texture_classes,
                            options= texture_classes,
                            max_selections=7
                        )
                    elif dataset1_name:
                        dataset1_range = st.slider(
                            f"Filter {dataset1_name}",
                            min_value=soil_functions.get_datasets_min_max(dataset1_name)[0],
                            max_value=soil_functions.get_datasets_min_max(dataset1_name)[1],
                            value=(soil_functions.get_datasets_min_max(dataset1_name)[0],
                            soil_functions.get_datasets_min_max(dataset1_name)[1])
                        )
                    if dataset1_name:
                        selected_datasets.update({dataset1_name:list(dataset1_range)})

                with col2b:
                    if dataset2_name == 'Texture Class':
                        dataset2_range = st.multiselect(
                            f"Filter {dataset2_name}",
                            texture_classes, max_selections=3
                        )
                    elif dataset2_name:
                        dataset2_range = st.slider(
                            f"Filter {dataset2_name}",
                            min_value = soil_functions.get_datasets_min_max(dataset2_name)[0],
                            max_value = soil_functions.get_datasets_min_max(dataset2_name)[1],
                            value = (soil_functions.get_datasets_min_max(dataset2_name)[0],
                            soil_functions.get_datasets_min_max(dataset2_name)[1])
                        )
                    if dataset2_name:
                        selected_datasets.update({dataset2_name:list(dataset2_range)})

                if dataset2_name:
                    with col3b:
                        if dataset3_name == 'Texture Class':
                            dataset3_range = st.multiselect(
                                f"Filter {dataset3_name}",
                                texture_classes, max_selections=3
                            )
                        elif dataset3_name:
                            dataset3_range = st.slider(
                                f"Filter {dataset3_name}",
                                min_value = soil_functions.get_datasets_min_max(dataset3_name)[0],
                                max_value = soil_functions.get_datasets_min_max(dataset3_name)[1],
                                value = (soil_functions.get_datasets_min_max(dataset3_name)[0],
                                soil_functions.get_datasets_min_max(dataset3_name)[1])
                            )
                        if dataset3_name:
                            selected_datasets.update({dataset3_name:list(dataset3_range)})

                if dataset2_name and dataset3_name:
                    with col4b:
                        if dataset4_name == 'Texture Class':
                            dataset4_range = st.multiselect(
                                f"Filter {dataset4_name}",
                                texture_classes, max_selections=3
                            )
                        elif dataset4_name:
                            dataset4_range = st.slider(
                                f"Filter {dataset4_name}",
                                min_value = soil_functions.get_datasets_min_max(dataset4_name)[0],
                                max_value = soil_functions.get_datasets_min_max(dataset4_name)[1],
                                value = (soil_functions.get_datasets_min_max(dataset4_name)[0],
                                soil_functions.get_datasets_min_max(dataset4_name)[1])
                            )
                        if dataset4_name:
                            selected_datasets.update({dataset4_name:list(dataset4_range)})

                if dataset2_name and dataset3_name and dataset4_name:
                    with col5b:
                        if dataset5_name == 'Texture Class':
                            dataset5_range = st.multiselect(
                                f"Filter {dataset5_name}",
                                texture_classes, max_selections=3
                            )
                        elif dataset5_name:
                            dataset5_range = st.slider(
                                f"Filter {dataset5_name}",
                                min_value = soil_functions.get_datasets_min_max(dataset5_name)[0],
                                max_value = soil_functions.get_datasets_min_max(dataset5_name)[1],
                                value = (soil_functions.get_datasets_min_max(dataset5_name)[0],
                                soil_functions.get_datasets_min_max(dataset5_name)[1])
                            )
                        if dataset5_name:
                            selected_datasets.update({dataset5_name:list(dataset5_range)})

            if dataset1_name:
                with st.spinner(f"Getting {dataset1_name}...", show_time=True):
                    overlaid_dataset = soil_functions.get_overlaid_dataset(selected_datasets, aoi_gdf)

            if len(selected_datasets) > 1:
                palette = ["#009100", "#00ff00", "#FBFF00", "#ff0000", "#770000"]
                overlaid_palette = palette[:len(selected_datasets)]
                overlaid_palette = overlaid_palette[::-1]
                overlaid_names = [rank + 1 for rank in range(len(selected_datasets))]
                overlaid_visparams = {'min': 1, 'max': len(selected_datasets), 'palette': overlaid_palette}
            else:
                if dataset1_name == 'Texture Class':
                    overlaid_visparams, overlaid_texture_names, overlaid_texture_palette = soil_functions. \
                                                get_soil_dataset_visparams(dataset1_name, overlaid_dataset)
                elif dataset1_name and dataset1_range:
                    overlaid_visparams = soil_functions.get_soil_dataset_visparams(dataset1_name, overlaid_dataset)
                    overlaid_visparams ['min'] = dataset1_range[0]
                    overlaid_visparams ['max'] = dataset1_range[1]

        else:
            if dataset1_name:
                with st.spinner(f"Getting {dataset1_name}...", show_time=True):
                    soil_dataset = soil_functions.get_soil_dataset(aoi_gdf)[dataset1_name]
                    if dataset1_name == 'Texture Class':
                        visparams, texture_names, texture_palette = soil_functions.get_soil_dataset_visparams(dataset1_name, soil_dataset)
                    else:
                        visparams = soil_functions.get_soil_dataset_visparams(dataset1_name, soil_dataset)

        with st.spinner("Analysing soil properties...", show_time=True):
            m = geemap_folium.Map(control_scale=True, draw_control=False, layer_control=False)

            m.add_ee_layer = ee_functions.add_ee_layer.__get__(m)
            
            m.add_child(MeasureControl(
                primary_length_unit='kilometers',
                secondary_length_unit='meters',
                primary_area_unit='sqmeters',
                secondary_area_unit='hectares'
            ))

            m.add_basemap('CartoDB.DarkMatter',False)
            m.add_gdf(aoi_gdf, layer_name="Zambia", info_mode="on_click")

            if dataset1_name and not toggle:
                m.add_ee_layer(soil_dataset, visparams=visparams, name=dataset1_name)

                if dataset1_name == 'Texture Class':
                    legend_dict = dict(zip(texture_names, texture_palette))
                    soil_functions.add_categorical_legend(m, "Soil Texture", list(legend_dict.values()), list(legend_dict.keys()))
                    # m.add_legend(
                    #     legend_dict=legend_dict,
                    #     position="bottomright",
                    #     title=f"Soil {dataset1_name}",
                    #     draggable=True
                    # )
                else:
                    soil_functions.add_vertical_colorbar(m, dataset1_name, visparams['min'], visparams['max'], visparams['palette'])
                    # m.add_colorbar(
                    #     visparams,
                    #     label=dataset1_name,
                    #     orientation='vertical'
                    #     )

            elif dataset1_name and toggle and dataset1_range:
                m.add_ee_layer(overlaid_dataset, visparams=overlaid_visparams, name=dataset1_name)

                if dataset1_name == 'Texture Class' and len(selected_datasets) == 1:
                    legend_dict = dict(zip(overlaid_texture_names[::-1], overlaid_texture_palette[::-1]))
                    soil_functions.add_categorical_legend(m, "Soil Texture", list(legend_dict.values()), list(legend_dict.keys()))
                    # m.add_legend(
                    #     legend_dict=legend_dict,
                    #     position="bottomright",
                    #     title=f"Soil {dataset1_name}",
                    #     draggable=True
                    # )
                elif len(selected_datasets) > 1:
                    legend_dict = dict(zip(overlaid_names[::-1], overlaid_palette[::-1]))
                    soil_functions.add_categorical_legend(m, "Suitability Rank", list(legend_dict.values()), list(legend_dict.keys()))
                    # m.add_legend(
                    #     legend_dict=legend_dict,
                    #     position="bottomright",
                    #     title="Suitability Rank",
                    #     draggable=True
                    # )
                else:
                    soil_functions.add_vertical_colorbar(m, dataset1_name, overlaid_visparams['min'], overlaid_visparams['max'], overlaid_visparams['palette'])
                    # m.add_colorbar(
                    #     overlaid_visparams,
                    #     label=dataset1_name,
                    #     orientation='vertical'
                    #     )

            m.zoom_to_gdf(aoi_gdf)

            m.to_streamlit(height=550)
