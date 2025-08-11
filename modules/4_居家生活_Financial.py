# modules/6_居家生活_Financial.py

import streamlit as st
import pandas as pd
import plotly.express as px
import os
from finmind_tools import (
    analyze_csv_to_wide_df,
    run_buffett_column1_analysis,
    run_buffett_column2_analysis,
    run_cashflow_column3_analysis 
)
from language_config import get_text

# --- Load and pivot the CSV using the reusable tool ---
try:
    df_wide_居家生活 = analyze_csv_to_wide_df("finmind_data/居家生活.csv")
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

df_original_居家生活 = analyze_csv_to_wide_df("finmind_data/居家生活.csv")

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(get_text('balance_sheet_analysis'))
    st.markdown(f"#### {get_text('buffett_balance_sheet_rule')}")
    st.caption(get_text('balance_sheet_rule_desc'))

    results_居家生活 = run_buffett_column1_analysis(df_original_居家生活.copy())

    df_wide_bal_居家生活 = results_居家生活["df_wide"]
    df_top5_bal_居家生活 = results_居家生活["df_top5"]
    fig_bal_居家生活 = results_居家生活["fig_heatmap"]
    fig1_居家生活 = results_居家生活["fig1"]
    fig2_居家生活 = results_居家生活["fig2"]
    fig3_居家生活 = results_居家生活["fig3"]
    fig4_居家生活 = results_居家生活["fig4"]
    ranking_bal_居家生活 = results_居家生活["ranking_df"]

    st.plotly_chart(fig_bal_居家生活, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_balance_sheet')}")
    st.plotly_chart(fig1_居家生活, use_container_width=True)
    st.plotly_chart(fig2_居家生活, use_container_width=True)
    st.plotly_chart(fig3_居家生活, use_container_width=True)
    st.plotly_chart(fig4_居家生活, use_container_width=True)

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_balance_sheet')}")
    st.dataframe(ranking_bal_居家生活, use_container_width=True)

#=========================================================================================================
with col2:
    st.subheader(get_text('income_statement_analysis'))
    st.markdown(f"#### {get_text('buffett_income_rule')}")
    st.caption(get_text('income_rule_desc'))

    # --- Run tool and unpack ---
    results_inc_居家生活 = run_buffett_column2_analysis(df_original_居家生活.copy())

    df_wide_inc_居家生活 = results_inc_居家生活["df_wide"]
    df_top5_inc_居家生活 = results_inc_居家生活["df_top5_inc"]
    fig_income_居家生活 = results_inc_居家生活["fig_income"]
    fig1_居家生活 = results_inc_居家生活["fig1_inc"]
    fig2_居家生活 = results_inc_居家生活["fig2_inc"]
    fig3_居家生活 = results_inc_居家生活["fig3_inc"]
    fig4_居家生活 = results_inc_居家生活["fig4_inc"]
    ranking_inc_居家生活 = results_inc_居家生活["ranking_inc"]

    # --- Show Plotly Heatmap ---
    st.plotly_chart(fig_income_居家生活, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_income_statement')}")
    st.plotly_chart(fig1_居家生活, use_container_width=True)
    st.plotly_chart(fig2_居家生活, use_container_width=True)
    st.plotly_chart(fig3_居家生活, use_container_width=True)
    st.plotly_chart(fig4_居家生活, use_container_width=True)

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_income_statement')}")
    st.dataframe(ranking_inc_居家生活, use_container_width=True)

#=========================================================================================================
with col3:
    st.subheader(get_text('cash_flow_analysis'))
    st.markdown(f"#### {get_text('feroldi_cash_flow_rule')}")
    st.caption(get_text('cash_flow_rule_desc_detailed'))

    results_cf_居家生活 = run_cashflow_column3_analysis(df_original_居家生活.copy())

    # --- Heatmap ---
    st.plotly_chart(results_cf_居家生活["fig_heatmap"], use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_cash_flow')}")
    st.plotly_chart(results_cf_居家生活["fig1"], use_container_width=True)
    st.plotly_chart(results_cf_居家生活["fig2"], use_container_width=True)
    st.plotly_chart(results_cf_居家生活["fig3"], use_container_width=True)
    st.plotly_chart(results_cf_居家生活["fig4"], use_container_width=True)
    st.plotly_chart(results_cf_居家生活["fig5"], use_container_width=True)
    st.plotly_chart(results_cf_居家生活["fig6"], use_container_width=True)

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_cash_flow')}")
    st.dataframe(results_cf_居家生活["ranking_df"], use_container_width=True)

from finmind_tools import register_industry_rankings

register_industry_rankings(
    industry_name="居家生活",
    bal_df=ranking_bal_居家生活,
    inc_df=ranking_inc_居家生活,
    cf_df=results_cf_居家生活["ranking_df"]
)