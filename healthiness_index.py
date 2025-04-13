import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.sidebar.header("Upload Your Data")
healthiness_index = st.sidebar.file_uploader("Upload CSV File Healthiness Index", type=["csv"], key="healthiness_index")
okr = st.sidebar.file_uploader("Upload CSV File Related OKR Target", type=["csv"], key="OKR")

def get_final_data():
    df = pd.read_csv(healthiness_index, index_col=0)
    df['yearweek'] = df['yearweek'].astype(str)
    df.rename(columns={'location': 'city'}, inplace=True)
    return df.set_index(['yearweek', 'city', 'region'])

def get_okr():
    df = pd.read_csv(okr, index_col=0)
    df.rename(columns={'location': 'city'}, inplace=True)
    return df.set_index(['yearweek', 'city', 'region'])

st.title('''
            City Healthiness Index
         ''')

try:
    df = get_final_data()
    st.sidebar.header('Filter Data')

    # healthiness_index
    healthiness_index = df[['Healthiness_Index_(%)']]

    yearweek_list = sorted(healthiness_index.index.get_level_values('yearweek').unique())
    selected_yearweek = st.sidebar.multiselect('yearweek', yearweek_list)

    if selected_yearweek:
        yearweek_hi = healthiness_index[healthiness_index.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_hi = healthiness_index

    region_list = sorted(yearweek_hi.index.get_level_values('region').unique())
    selected_region = st.sidebar.multiselect('region', region_list)

    if selected_region:
        region_hi = yearweek_hi[yearweek_hi.index.get_level_values('region').isin(selected_region)]
    else:
        region_hi = yearweek_hi

    city_list = sorted(region_hi.index.get_level_values('city').unique())
    selected_city = st.sidebar.multiselect('city', city_list)

    if selected_city:
        hi_value = region_hi[region_hi.index.get_level_values('city').isin(selected_city)]
    else:
        hi_value = region_hi
    
    # Daftar kategori HI (Healthiness Index)
    hi_ranges = {
        "25 - 34.99": (25, 34.99),
        "35 - 44.99": (35, 44.99),
        "50 - 54.99": (50, 54.99),
        "55 - 64.99": (55, 64.99),
        "65 - 74.55": (65, 74.55),
        "75 - 84.99": (75, 84.99),
        "85 - 94.55": (85, 94.55),
        "95 - 100": (95, 100),
    }

    selected_ranges = st.sidebar.multiselect("Healthiness Index Range", list(hi_ranges.keys()))

    if selected_city:
        healthiness_index_result = region_hi[region_hi.index.get_level_values('city').isin(selected_city)]
    else:
        healthiness_index_result = region_hi

    # Filter berdasarkan nilai HI range
    if selected_ranges:
        filtered_by_hi = pd.DataFrame()
        for label in selected_ranges:
            lower, upper = hi_ranges[label]
            filtered_part = healthiness_index_result[
                (healthiness_index_result['Healthiness_Index_(%)'] >= lower) &
                (healthiness_index_result['Healthiness_Index_(%)'] <= upper)
            ]
            filtered_by_hi = pd.concat([filtered_by_hi, filtered_part])

        healthiness_index_result = filtered_by_hi
        
        healthiness_index_city = list(healthiness_index_result.index.get_level_values('city').unique())
    else:
        healthiness_index_result = hi_value
        healthiness_index_city = []

    st.subheader('Healthiness Index Result')
    st.dataframe(healthiness_index_result, use_container_width=True)

    # visulasisasi line plot
    df_vis = healthiness_index_result.reset_index()

    fig = px.line(
        df_vis,
        x='yearweek',
        y='Healthiness_Index_(%)',
        color='city',
        markers=True
    )

    fig.update_layout(
        xaxis=dict(
            tickformat=".0f",
            title='yearweek'
        )
    )
    st.subheader('Tren Healthiness Index per City')
    st.plotly_chart(fig, use_container_width=True)

    # value kpi
    value_kpi = df.iloc[:, :13]

    if selected_yearweek:
        yearweek_df = value_kpi[value_kpi.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_df = value_kpi

    if selected_region:
        region_df = yearweek_df[yearweek_df.index.get_level_values('region').isin(selected_region)]
    else:
        region_df = yearweek_df

    if selected_city:
        value_kpi_df = region_df[region_df.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        value_kpi_df = region_df[region_df.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        value_kpi_df = region_df
    
    st.subheader('Raw Value KPI')
    st.dataframe(value_kpi_df, use_container_width=True)

    # alert_status
    alert_status_kpi = df.iloc[:, 14:26]
 
    if selected_yearweek:
        yearweek_status = alert_status_kpi[alert_status_kpi.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_status = alert_status_kpi

    if selected_region:
        region_status = yearweek_status[yearweek_status.index.get_level_values('region').isin(selected_region)]
    else:
        region_status = yearweek_df

    if selected_city:
        status_kpi = region_status[region_status.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        status_kpi = region_status[region_status.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        status_kpi = region_status
    
    st.subheader('Alert Status KPI')
    st.dataframe(status_kpi, use_container_width=True)

    # okr
    okr = get_okr()

    if selected_yearweek:
        yearweek_okr = okr[okr.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_okr = okr

    if selected_region:
        region_okr = yearweek_okr[yearweek_okr.index.get_level_values('region').isin(selected_region)]
    else:
        region_okr = yearweek_okr

    if selected_city:
        okr_city = region_okr[region_okr.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        okr_city = region_okr[region_okr.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        okr_city = region_okr
    
    st.subheader('Related OKR Target Q1')
    st.dataframe(okr_city, use_container_width=True)

    # alert_target
    alert_target_kpi = df.iloc[:, 26:38]
 
    if selected_yearweek:
        yearweek_target = alert_target_kpi[alert_target_kpi.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_target = alert_target_kpi

    if selected_region:
        region_target = yearweek_target[yearweek_target.index.get_level_values('region').isin(selected_region)]
    else:
        region_target = yearweek_target

    if selected_city:
        target_kpi = region_target[region_target.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        target_kpi= region_target[region_target.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        target_kpi = region_target
    
    st.subheader('Alert Target KPI')
    st.dataframe(target_kpi, use_container_width=True)

    # alert result
    alert_result = df.iloc[:, 38:50]

    if selected_yearweek:
        yearweek_result = alert_result[alert_result.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_result = alert_result

    if selected_region:
        region_result = yearweek_result[yearweek_result.index.get_level_values('region').isin(selected_region)]
    else:
        region_result = yearweek_result

    if selected_city:
        result_alert = region_result[region_result.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        result_alert = region_result[region_result.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        result_alert = region_result
    
    st.subheader('Result Alert')
    st.dataframe(result_alert, use_container_width=True)

    # score
    score = df.iloc[:, 62:74]

    if selected_yearweek:
        yearweek_score = score[score.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_score = score

    if selected_region:
        region_score = yearweek_score[yearweek_score.index.get_level_values('region').isin(selected_region)]
    else:
        region_score = yearweek_score

    if selected_city:
        result_score = region_score[region_score.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        result_score = region_score[region_score.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        result_score = region_score
    
    st.subheader('Score')
    st.dataframe(result_score, use_container_width=True)

    # feature importance
    fi = df.iloc[:, 50:62]

    if selected_yearweek:
        yearweek_fi = fi[fi.index.get_level_values('yearweek').isin(selected_yearweek)]
    else:
        yearweek_fi = fi

    if selected_region:
        region_fi = yearweek_fi[yearweek_fi.index.get_level_values('region').isin(selected_region)]
    else:
        region_fi = yearweek_fi

    if selected_city:
        feature_importance = region_fi[region_fi.index.get_level_values('city').isin(selected_city)]
    elif selected_ranges:
        feature_importance = region_df[region_df.index.get_level_values('city').isin(healthiness_index_city)]
    else:
        feature_importance = region_fi
    
    st.subheader('Feature Importance')
    st.dataframe(feature_importance, use_container_width=True)

except Exception as e:
    print(f"Terjadi error saat memuat data: {e}")