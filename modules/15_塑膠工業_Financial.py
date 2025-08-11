# modules/19_塑膠工業_Financial.py

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
    df_wide_塑膠工 = analyze_csv_to_wide_df("finmind_data/塑膠工業.csv")
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

df_original_塑膠工 = analyze_csv_to_wide_df("finmind_data/塑膠工業.csv")

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(get_text('balance_sheet_analysis'))
    st.markdown(f"#### {get_text('buffett_balance_sheet_rule')}")
    st.caption(get_text('balance_sheet_rule_desc'))

    results_塑膠工 = run_buffett_column1_analysis(df_original_塑膠工.copy())

    df_wide_bal_塑膠工 = results_塑膠工["df_wide"]
    df_top5_bal_塑膠工 = results_塑膠工["df_top5"]
    fig_bal_塑膠工 = results_塑膠工["fig_heatmap"]
    fig1_塑膠工 = results_塑膠工["fig1"]
    fig2_塑膠工 = results_塑膠工["fig2"]
    fig3_塑膠工 = results_塑膠工["fig3"]
    fig4_塑膠工 = results_塑膠工["fig4"]
    ranking_bal_塑膠工 = results_塑膠工["ranking_df"]

    st.plotly_chart(fig_bal_塑膠工, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_balance_sheet')}")
    st.plotly_chart(fig1_塑膠工, use_container_width=True)
    st.plotly_chart(fig2_塑膠工, use_container_width=True)
    st.plotly_chart(fig3_塑膠工, use_container_width=True)
    st.plotly_chart(fig4_塑膠工, use_container_width=True)

    # --- Balance Sheet Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_balance_sheet')}")
    st.dataframe(ranking_bal_塑膠工, use_container_width=True)

with col2:
    st.subheader(get_text('income_statement_analysis'))
    st.markdown(f"#### {get_text('buffett_income_rule')}")
    st.caption(get_text('income_rule_desc'))

    results2_塑膠工 = run_buffett_column2_analysis(df_original_塑膠工.copy())

    df_wide_inc_塑膠工 = results2_塑膠工["df_wide"]
    df_top5_inc_塑膠工 = results2_塑膠工["df_top5_inc"]
    fig_inc_塑膠工 = results2_塑膠工["fig_income"]
    fig5_塑膠工 = results2_塑膠工["fig1_inc"]
    fig6_塑膠工 = results2_塑膠工["fig2_inc"]
    fig7_塑膠工 = results2_塑膠工["fig3_inc"]
    fig8_塑膠工 = results2_塑膠工["fig4_inc"]
    ranking_inc_塑膠工 = results2_塑膠工["ranking_inc"]

    st.plotly_chart(fig_inc_塑膠工, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_income_statement')}")
    st.plotly_chart(fig5_塑膠工, use_container_width=True)
    st.plotly_chart(fig6_塑膠工, use_container_width=True)
    st.plotly_chart(fig7_塑膠工, use_container_width=True)
    st.plotly_chart(fig8_塑膠工, use_container_width=True)

    # --- Income Statement Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_income_statement')}")
    st.dataframe(ranking_inc_塑膠工, use_container_width=True)

with col3:
    st.subheader(get_text('cash_flow_analysis'))
    st.markdown(f"#### {get_text('feroldi_cash_flow_rule')}")
    st.caption(get_text('cash_flow_rule_desc_detailed'))

    results3_塑膠工 = run_cashflow_column3_analysis(df_original_塑膠工.copy())

    df_wide_cash_塑膠工 = results3_塑膠工["df_wide"]
    df_top5_cash_塑膠工 = results3_塑膠工["df_top5"]
    fig_cash_塑膠工 = results3_塑膠工["fig_heatmap"]
    fig9_塑膠工 = results3_塑膠工["fig1"]
    fig10_塑膠工 = results3_塑膠工["fig2"]
    fig11_塑膠工 = results3_塑膠工["fig3"]
    fig12_塑膠工 = results3_塑膠工["fig4"]
    ranking_cash_塑膠工 = results3_塑膠工["ranking_df"]

    st.plotly_chart(fig_cash_塑膠工, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_cash_flow')}")
    st.plotly_chart(fig9_塑膠工, use_container_width=True)
    st.plotly_chart(fig10_塑膠工, use_container_width=True)
    st.plotly_chart(fig11_塑膠工, use_container_width=True)
    st.plotly_chart(fig12_塑膠工, use_container_width=True)

    # --- Cash Flow Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_cash_flow')}")
    st.dataframe(ranking_cash_塑膠工, use_container_width=True)

# --- Register rankings for Stock Agent ---
from finmind_tools import register_industry_rankings

register_industry_rankings(
    industry_name="塑膠工業",
    bal_df=ranking_bal_塑膠工,
    inc_df=ranking_inc_塑膠工,
    cf_df=ranking_cash_塑膠工
)