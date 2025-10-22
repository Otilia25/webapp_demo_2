import streamlit as st
import random
import folium
from folium.plugins import MarkerCluster
import altair as alt

def add_sh_location_filter_selectboxes(gdf):
    region_col, district_col, hub_col, camp_col, = st.columns([3, 3, 3, 3])

    with region_col:
        regions = sorted(gdf['region'].dropna().unique())
        selected_region = st.selectbox(
            "Region", regions, index=None, placeholder="Select region...", key=30
            )

    filtered_df = gdf.copy()
    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    with district_col:
        districts = sorted(filtered_df['district'].dropna().unique())
        selected_district = st.selectbox(
            "District", districts, index=None, placeholder="Select district...", key=31
            )

    if selected_district:
        filtered_df = filtered_df[filtered_df['district'] == selected_district]

    with hub_col:
        hubs = sorted(filtered_df['hub'].dropna().unique())
        selected_hub = st.selectbox(
            "Hub", hubs, index=None, placeholder="Select hub...", key=32
            )

    if selected_hub:
        filtered_df = filtered_df[filtered_df['hub'] == selected_hub]

    with camp_col:
        camps = sorted(filtered_df['camp'].dropna().unique())
        selected_camp = st.selectbox(
            "Camp", camps, index=None, placeholder="Select camp...", key=33
            )

    if selected_camp:
        filtered_df = filtered_df[filtered_df['camp'] == selected_camp]

    return selected_region, selected_district, selected_hub, selected_camp

def add_sh_personnel_filter_selectboxes(gdf):
    fs_col, pea_col, farmer_col = st.columns([3, 3, 3])

    filtered_df = gdf.copy()

    with fs_col:
        fss = sorted(filtered_df['fs'].dropna().unique())
        selected_fs = st.selectbox(
            "FS", fss, index=None, placeholder="Select FS...", key=34
            )

    if selected_fs:
        filtered_df = filtered_df[filtered_df['fs'] == selected_fs]

    with pea_col:
        peas = sorted(filtered_df['pea'].dropna().unique())
        selected_pea = st.selectbox(
            "PEA", peas, index=None, placeholder="Select PEA...", key=35
            )

    if selected_pea:
        filtered_df = filtered_df[filtered_df['pea'] == selected_pea]

    with farmer_col:
        selected_farmer_id = st.number_input(
            "Farmer ID", placeholder="Enter Farmer ID...", format="%0f", key=36
            )

    return selected_fs, selected_pea, selected_farmer_id

def get_filtered_gdf(gdf, selected_region, selected_district, selected_hub, selected_camp, selected_fs, selected_pea, selected_farmer_id):
    filtered_df = gdf.copy()
    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    if selected_district:
        filtered_df = filtered_df[filtered_df['district'] == selected_district]

    if selected_hub:
        filtered_df = filtered_df[filtered_df['hub'] == selected_hub]

    if selected_camp:
        filtered_df = filtered_df[filtered_df['camp'] == selected_camp]

    if selected_fs:
        filtered_df = filtered_df[filtered_df['fs'] == selected_fs]

    if selected_pea:
        filtered_df = filtered_df[filtered_df['pea'] == selected_pea]

    if selected_farmer_id:
        filtered_df = filtered_df[filtered_df['farmer_id'] == selected_farmer_id]

    return filtered_df

def get_colors(selected_color_by, filtered_gdf):
    rename_selected_color_by = {'Region': 'region_id', 'District': 'district_id', 'Hub': 'hub_id',
                        'Camp': 'camp_id', 'FS': 'fs_id', 'PEA': 'pea_id'}

    if selected_color_by == 'Region':
        color_options = {
            2: "#0000C9", 1: "#A700A7", 7: "#009100", 9: '#ff0000',4: "#0066ff",
            13: "#ff9900", 11: '#ffffff', 12: "#ccbe00", 5: "#583500", 3: "#ff6f6f", 6: "#7a0000", 8: "#a1ff55"
        }

        values_list = filtered_gdf[rename_selected_color_by[selected_color_by]].unique().tolist()
        colors = {}
        for value in values_list:
            value_color = {value: color_options[value]}
            colors.update(value_color)

    else:
        colors = {}
        random.seed(42)
        values_list = filtered_gdf[rename_selected_color_by[selected_color_by]].unique().tolist()
        
        for value in values_list:
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            value_color = {value: color}
            colors.update(value_color)

    return colors

def get_scorecards(filtered_gdf):
    region_col, district_col, hub_col, camp_col, fs_col, pea_col, farmer_col = st.columns(7)

    region_metric = region_col.metric(
        "Regions", filtered_gdf['region_id'].nunique(), border=True
        )
    district_metric = district_col.metric(
        "Districts", filtered_gdf['district_id'].nunique(), border=True
        )
    hub_metric = hub_col.metric(
        "Hubs", filtered_gdf['hub'].nunique(), border=True
        )
    camp_metric = camp_col.metric(
        "Camps", filtered_gdf['camp_id'].nunique(), border=True
        )
    fs_metric = fs_col.metric(
        "FSs", filtered_gdf['fs_id'].nunique(), border=True
        )
    pea_metric = pea_col.metric(
        "PEAs", filtered_gdf['pea_id'].nunique(), border=True
        )
    farmer_metric = farmer_col.metric(
        "Fields", filtered_gdf['field_id'].nunique(), border=True
        )

    return region_metric, district_metric, hub_metric, camp_metric, fs_metric, pea_metric, farmer_metric

def get_selected_chart_options():
    category_options = ['Region', 'District', 'Hub', 'Camp', 'FS', 'PEA']
    value_options = {'District': 'district_id', 'Hub': 'hub_id', 'Camp': 'camp_id',
                    'FS': 'fs_id', 'PEA': 'pea_id', 'Field': 'field_id'}

    selected_category = st.selectbox(
        "Select category", category_options, index=0, key=37
        )
    selected_sub_category = st.selectbox(
        "Select sub-category (optional)", value_options.keys(), index=None, key=38
        )
    selected_value = st.selectbox(
        "Select value", value_options.keys(), index=len(value_options)-1, key=39
        )

    return selected_category, selected_sub_category, selected_value

def get_altair_chart(filtered_gdf, selected_color_by, gotten_colors):
    renamed_gdf = filtered_gdf.rename(columns={
            'region': 'Region', 'district': 'District', 'hub': 'Hub',
            'camp': 'Camp', 'fs': 'FS', 'pea': 'PEA'
            })

    value_options = {'Region':'region_id', 'District': 'district_id', 'Hub': 'hub_id', 'Camp': 'camp_id',
                    'FS': 'fs_id', 'PEA': 'pea_id', 'Field': 'field_id'}

    chart_col, chart_selectors_col = st.columns([4,1])
    with chart_selectors_col:
        selected_category, selected_sub_category, selected_value = get_selected_chart_options()

    if selected_sub_category is not None:
        df = renamed_gdf.groupby([value_options[selected_sub_category], selected_category, selected_sub_category]) \
                .agg(**{selected_value: (value_options[selected_value], 'nunique')}) \
                .reset_index().sort_values(
                    [selected_value, selected_category], ascending=[False,  True]
                    )
        df.rename(columns={selected_value: f"{selected_value}s"}, inplace=True)

    else:
        df = renamed_gdf.groupby([value_options[selected_category], selected_category]) \
                .agg(**{selected_value: (value_options[selected_value], 'nunique')}) \
                .reset_index().sort_values(
                    [selected_value, selected_category], ascending=[False,  True]
                    )
        df.rename(columns={selected_value: f"{selected_value}s"}, inplace=True)

    renamed_value = f"{selected_value}s"

    # Calculate total count
    total_count = df[renamed_value].sum()

    # Add formatted percentage column
    if total_count > 0:
        df["Percentage"] = df[renamed_value].apply(
            lambda renamed_value: f"{(renamed_value / total_count) * 100:.1f}%")
    else:
        df["Percentage"] = "0.0%"

    if selected_sub_category is not None or selected_color_by == selected_sub_category:
        gotten_colors = get_colors(selected_sub_category, filtered_gdf)
        color_domain = list(gotten_colors.keys())
        color_range = list(gotten_colors.values())
    elif selected_color_by == selected_category:
        df['color'] = df[value_options[selected_category]].map(gotten_colors)
    else:
        df['color'] = "#94ff86"

    if selected_sub_category is None:
        tooltips=[
                alt.Tooltip(f'{selected_category}:N'),
                alt.Tooltip(f'{renamed_value}:Q'),
                alt.Tooltip('Percentage:N')
                ]
    else:
        tooltips=[
                alt.Tooltip(f'{selected_category}:N'),
                alt.Tooltip(f'{selected_sub_category}:N'),
                alt.Tooltip(f'{renamed_value}:Q'),
                alt.Tooltip('Percentage:N')
                ]

    # Define custom order
    # Aggregate total value per category
    category_order = (
            df.groupby(selected_category)[renamed_value]
            .sum()
            .sort_values(ascending=False)
            .index.tolist()
        )
    if selected_sub_category is not None:
        subcat_order = (
            df.groupby(selected_sub_category)[renamed_value]
            .sum()
            .sort_values(ascending=False)
            .index.tolist()
        )
        # custom_order = sorted(df[renamed_value].to_list())

    if selected_sub_category is not None:
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f'{renamed_value}:Q', stack='zero'),
            y=alt.Y(f'{selected_category}:N', sort=category_order),
            color=alt.Color(
                f'{value_options[selected_sub_category]}:N', legend=None, sort=subcat_order,
                scale=alt.Scale(domain=color_domain, range=color_range)),
            tooltip=tooltips
        ).properties(width=500, height=alt.Step(30))
    else:
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f'{renamed_value}:Q'),
            y=alt.Y(f'{selected_category}:N', sort=category_order),
            color=alt.Color('color:N', scale=None, legend=None),
            tooltip=tooltips
        ).properties(width=500, height=alt.Step(30))

    with chart_col:
        altair_chart = st.altair_chart(chart)

    return altair_chart, selected_category, selected_sub_category, selected_value 

def add_map_cicle_markers(filtered_gdf, gotten_colors, selected_color_by, rename_color_by, marker_cluster):
    # Add points as circle markers
    for _, row in filtered_gdf.iterrows():
        tooltip_text = (
            f"<b>Farmer ID:</b> {row['farmer_id']}<br>"
            f"<b>Camp:</b> {row['camp']}<br>"
            f"<b>PEA:</b> {row['pea']}<br>"
            f"<b>Hub:</b> {row['hub']}<br>"
            f"<b>FS:</b> {row['fs']}<br>"
            f"<b>District:</b> {row['district']}<br>"
            f"<b>Region:</b> {row['region']}"
        )

        if gotten_colors is None:
            color = '#ffffff'
        else:
            color = gotten_colors.get(row[rename_color_by[selected_color_by]], '#ffffff')

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=1,
            tooltip=folium.Tooltip(tooltip_text, sticky=True),
            color=color,
        ).add_to(marker_cluster)