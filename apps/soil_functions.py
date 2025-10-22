import streamlit as st
import math
import ee
import geemap
import geopandas as gpd
from branca.element import Template, MacroElement

def get_soil_dataset(selected_aoi_gdf):
    if selected_aoi_gdf is None:
        soil_datasets = [
            "Annual Rainfall (mm)", "Texture Class", "pH", "Clay Content (%)", "Sand Content (%)",
            "Stone Content (%)", "Silt Content (%)", "Carbon Organic (g/kg)", "Carbon Total (g/kg)",
            "Nitrogen Total (g/kg)", "Potassium Extractable (ppm)", "Phosphorus Extractable (ppm)",
            "Magnesium Extractable (ppm)", "Iron Extractable (ppm)", "Zinc Extractable (ppm)",
            "Calcium Extractable (ppm)", "Sulphur Extractable (ppm)", "Aluminium Extractable (ppm)",
            "Effective Cation Exchange Capacity (cmol(+)/kg)"
        ]
        return soil_datasets
    else:
        aoi_ee = geemap.gdf_to_ee(selected_aoi_gdf)
        soil_datasets = {
            "Annual Rainfall (mm)": get_avg_rainfall(2019, 2024, aoi_ee),
            "Texture Class": ee.Image("ISDASOIL/Africa/v1/texture_class").clip(aoi_ee).select(0),
            "pH": ee.Image("ISDASOIL/Africa/v1/ph").clip(aoi_ee).select(0).divide(10),
            "Clay Content (%)": ee.Image("ISDASOIL/Africa/v1/clay_content").clip(aoi_ee).select(0),
            "Sand Content (%)": ee.Image("ISDASOIL/Africa/v1/sand_content").clip(aoi_ee).select(0),
            "Stone Content (%)": ee.Image("ISDASOIL/Africa/v1/stone_content").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Silt Content (%)": ee.Image("ISDASOIL/Africa/v1/silt_content").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Carbon Organic (g/kg)": ee.Image("ISDASOIL/Africa/v1/carbon_organic").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Carbon Total (g/kg)": ee.Image("ISDASOIL/Africa/v1/carbon_total").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Nitrogen Total (g/kg)": ee.Image("ISDASOIL/Africa/v1/nitrogen_total").clip(aoi_ee).select(0).divide(100).exp().subtract(1),
            "Potassium Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/potassium_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Phosphorus Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Magnesium Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/magnesium_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Iron Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/iron_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Zinc Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/zinc_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Calcium Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/calcium_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Sulphur Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/sulphur_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Aluminium Extractable (ppm)": ee.Image("ISDASOIL/Africa/v1/aluminium_extractable").clip(aoi_ee).select(0).divide(10).exp().subtract(1),
            "Effective Cation Exchange Capacity (cmol(+)/kg)": ee.Image("ISDASOIL/Africa/v1/cation_exchange_capacity").clip(aoi_ee).select(0).divide(10).exp().subtract(1)
        }
        return soil_datasets

def get_soil_dataset_visparams(selected_dataset_name, selected_dataset):
    if selected_dataset_name == 'Texture Class':
        class_colors = {
                1: ['Clay', "#d5c36b"],
                2: ['Silty Clay', '#b96947'],
                3: ['Sandy Clay', '#9d3706'],
                4: ['Clay Loam', '#ae868f'],
                5: ['Silty Clay Loam', '#f86714'],
                6: ['Sandy Clay Loam', "#46d143"],
                7: ['Loam', '#368f20'],
                8: ['Silt Loam', '#3e5a14'],
                9: ['Sandy Loam', "#ffd557"],
                10: ['Silt', '#fff72e'],
                11: ['Loamy Sand', '#ff5a9d'],
                12: ['Sand', '#ff005b']
            }
        texture_values = sorted(geemap.image_value_list(selected_dataset).getInfo())
        texture_values = [int(value) for value in texture_values]
        texture_values = sorted(texture_values)

        texture_names = [class_colors[int(x)][0] for x in texture_values]
        texture_palette = [class_colors[int(x)][1] for x in texture_values]
        visparams = {
            'min': int(texture_values[0]), 
            'max': int(texture_values[-1]), 
            'palette': texture_palette
        }
        return visparams, texture_names, texture_palette
    else:
        # min = geemap.image_min_value(selected_dataset, aoi_ee, 30)
        # max = geemap.image_max_value(selected_dataset, aoi_ee, 30)
        min = math.floor(get_datasets_min_max(selected_dataset_name)[0] * 100)/100.0
        max = math.ceil(get_datasets_min_max(selected_dataset_name)[1] * 100)/100.0
        visparams = {
                'min': min, #min.getInfo()['mean_0_20'], 
                'max': max, #max.getInfo()['mean_0_20'], 
                'palette': ["#000004", "#0C0927", "#231151", "#410F75",
                            "#5F187F", "#7B2382","#982D80", "#B63679",
                            "#D3436E", "#EB5760", "#F8765C", "#FD9969",
                            "#FEBA80", "#FDDC9E", "#FCFDBF"]
            }
        return visparams

def get_selected_datasets(selected_dataset_names_list, aoi_gdf):
    selected_datasets = []
    for selected_dataset_name in selected_dataset_names_list:
        selected_dataset = get_soil_dataset(aoi_gdf)[selected_dataset_name]
        selected_datasets.append(selected_dataset)
    return selected_datasets

def get_datasets_min_max(selected_dataset_name):
    dataset_min_max = {
        "Annual Rainfall (mm)": (400, 1600),
        'pH': (4.6, 7.6),
        'Clay Content (%)': (3.0, 53.0),
        'Sand Content (%)': (19.0, 90.0),
        'Stone Content (%)': (0.0, 5.0),
        'Silt Content (%)': (0.49182, 26.0),
        'Carbon Organic (g/kg)': (2.66929, 16.0),
        'Carbon Total (g/kg)': (2.66929, 48.402449),
        'Nitrogen Total (g/kg)': (0.28402, 1.7),
        'Potassium Extractable (ppm)': (10.023176, 400.0),
        'Phosphorus Extractable (ppm)': (3.05519, 20.0),
        'Magnesium Extractable (ppm)': (8.97418, 900.0),
        'Iron Extractable (ppm)': (30.0, 150.0),
        'Zinc Extractable (ppm)': (0.349858, 5.5),
        'Calcium Extractable (ppm)': (23.53253, 3050.0),
        'Sulphur Extractable (ppm)': (1.013752, 30.0),
        'Aluminium Extractable (ppm)': (17.17414, 300.0),
        'Effective Cation Exchange Capacity (cmol(+)/kg)': (1.22554, 35.0)
        }
    selected_dataset_min_max = dataset_min_max[selected_dataset_name]
    return selected_dataset_min_max

def get_filtered_dataset(selected_dataset_name, aoi_gdf, min_value, max_value, texture_classes):
    selected_dataset = get_soil_dataset(aoi_gdf)[selected_dataset_name]

    if selected_dataset_name == 'Texture Class':
        texture_values = {
                'Clay': 1, 'Silty Clay': 2, 'Sandy Clay': 3, 'Clay Loam': 4,
                'Silty Clay Loam': 5, 'Sandy Clay Loam': 6, 'Loam': 7, 'Silt Loam': 8,
                'Sandy Loam': 9, 'Silt': 10, 'Loamy Sand': 11, 'Sand': 12
            }

        mask = ee.Image(0)

        for selected_texture in texture_classes:
            texture_value = texture_values[selected_texture]
            texture_mask = selected_dataset.eq(texture_value)
            mask = mask.Or(texture_mask)

        filtered_dataset = selected_dataset.updateMask(mask)
        return filtered_dataset
    else:
        mask = selected_dataset.gte(min_value).And(selected_dataset.lte(max_value))
        filtered_dataset = selected_dataset.updateMask(mask)

        return filtered_dataset

def get_overlaid_dataset(selected_datasets, aoi_gdf):
    if len(selected_datasets) > 1:
        with st.spinner(f"Analysing soil properties...", show_time=True):
            aoi_ee = geemap.gdf_to_ee(aoi_gdf)
            overlaid_dataset = ee.Image(0).clip(aoi_ee)
            for dataset in selected_datasets:
                if dataset == 'Texture Class':
                    textures = selected_datasets[dataset]
                    filtered_dataset = get_filtered_dataset(dataset, aoi_gdf, None, None, textures)

                else:
                    min = selected_datasets[dataset][0]
                    max = selected_datasets[dataset][1]
                    filtered_dataset = get_filtered_dataset(dataset, aoi_gdf, min, max, None)

                binary_dataset = filtered_dataset.mask().gt(0)

                overlaid_dataset = overlaid_dataset.add(binary_dataset)

            overlaid_dataset = overlaid_dataset.updateMask(overlaid_dataset.gt(0))
            return overlaid_dataset
    else:
        dataset = selected_datasets
        name = list(dataset.keys())[0]
        if name == 'Texture Class':
            textures = dataset[list(dataset.keys())[0]]
            filtered_dataset = get_filtered_dataset(name, aoi_gdf, None, None, textures)

        else:
            min = dataset[list(dataset.keys())[0]][0]
            max = dataset[list(dataset.keys())[0]][1]
            filtered_dataset = get_filtered_dataset(name, aoi_gdf, min, max, None)
        return filtered_dataset

# Get images for rainy season (Nov to Mar) only
def get_rain_season_images(rainfall_dataset, start_year, end_year):
    # Create empty image collection
    merged_image_collection = ee.ImageCollection([])

    for year in range(start_year, end_year):
        # Nov to Dec of current year
        start1 = ee.Date(f'{year}-11-01')
        end1 = ee.Date(f'{year}-12-31')
        season_part1 = rainfall_dataset.filterDate(start1, end1)

        # Jan to Mar of following year
        start2 = ee.Date(f'{year + 1}-01-01')
        end2 = ee.Date(f'{year + 1}-03-31')
        season_part2 = rainfall_dataset.filterDate(start2, end2)

        # Merge image collection
        merged_year_collection = season_part1.merge(season_part2)
        merged_image_collection = merged_image_collection.merge(merged_year_collection)

    return merged_image_collection

def get_avg_rainfall(start_year, end_year, aoi_ee):

    rainfall_dataset = ee.ImageCollection("UCSB-CHG/CHIRPS/PENTAD") \
            .select('precipitation')

    no_years = end_year - start_year

    # Get images for rainfal season between selected dates
    seasonal_rainfall_dataset = get_rain_season_images(rainfall_dataset, start_year, end_year)

    # Clip images to AOI and compute the mean
    avg_rainfall = seasonal_rainfall_dataset.sum() \
                    .divide(no_years) \
                    .clip(aoi_ee)

    return avg_rainfall


def add_vertical_colorbar(m, title, min_val, max_val, palette):
    """Add a vertical continuous colorbar to a folium map matching the uploaded style."""

    gradient = f"linear-gradient(to top, {', '.join(palette)})"

    colorbar_html = f"""
    {{% macro html(this, kwargs) %}}
    <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        background-color: rgba(255,255,255,0.8);
        border: 1px solid #444;
        border-radius: 3px;
        padding: 5px;
        font-size: 11px;
        display: flex;
        align-items: center;
    ">
        <div style="position: relative; height: 200px; width: 15px;
                    background: {gradient};
                    border: 1px solid #999;
                    margin-right: 10px;">
            <div style="position: absolute; top: -6px; left: 100%; margin-left: 4px;">
                {max_val}
            </div>
            <div style="position: absolute; bottom: -6px; left: 100%; margin-left: 4px;">
                {min_val}
            </div>
        </div>
        <div style="
            writing-mode: vertical-rl;
            transform: rotate(180deg);
            margin-left: 8px;
            font-weight: bold;
        ">
            {title}
        </div>
    </div>
    {{% endmacro %}}
    """

    macro = MacroElement()
    macro._template = Template(colorbar_html)
    m.get_root().add_child(macro)
    return m

def add_categorical_legend(m, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    # Build legend items
    list_items = ""
    for color, label in zip(colors, labels):
        list_items += f"""
        <li><span style="background:{color}; opacity: 0.7"></span>{label}</li>
        """

    # HTML + CSS in a Jinja macro
    legend_html = f"""
    {{% macro html(this, kwargs) %}}
    <div id='maplegend' class='maplegend'
        style='
            position: fixed;
            z-index:9999;
            border: 2px solid grey;
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
            bottom: 20px;
            right: 20px;
        '>
        <div class='legend-title'>{title}</div>
        <div class='legend-scale'>
            <ul class='legend-labels'>
                {list_items}
            </ul>
        </div>
    </div>

    <style type='text/css'>
        .maplegend .legend-title {{
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
        }}
        .maplegend .legend-scale ul {{
            margin: 0;
            margin-bottom: 0px;
            padding: 0;
            float: left;
            list-style: none;
        }}
        .maplegend .legend-scale ul li {{
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 0px;
        }}
        .maplegend ul.legend-labels li span {{
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 1px solid #999;
        }}
        .maplegend .legend-source {{
            font-size: 80%;
            color: #777;
            clear: both;
        }}
        .maplegend a {{
            color: #777;
        }}
    </style>
    {{% endmacro %}}
    """

    macro = MacroElement()
    macro._template = Template(legend_html)
    m.get_root().add_child(macro)
    return m
