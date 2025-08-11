# modules/20_航運業_Financial.py

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
    df_wide_航運 = analyze_csv_to_wide_df("finmind_data/航運業.csv")
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

df_original_航運 = analyze_csv_to_wide_df("finmind_data/航運業.csv")

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(get_text('balance_sheet_analysis'))
    st.markdown(f"#### {get_text('buffett_balance_sheet_rule')}")
    st.caption(get_text('balance_sheet_rule_desc'))

    results_航運 = run_buffett_column1_analysis(df_original_航運.copy())

    df_wide_bal_航運 = results_航運["df_wide"]
    df_top5_bal_航運 = results_航運["df_top5"]
    fig_bal_航運 = results_航運["fig_heatmap"]
    fig1_航運 = results_航運["fig1"]
    fig2_航運 = results_航運["fig2"]
    fig3_航運 = results_航運["fig3"]
    fig4_航運 = results_航運["fig4"]
    ranking_bal_航運 = results_航運["ranking_df"]

    st.plotly_chart(fig_bal_航運, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_balance_sheet')}")
    st.plotly_chart(fig1_航運, use_container_width=True)
    st.plotly_chart(fig2_航運, use_container_width=True)
    st.plotly_chart(fig3_航運, use_container_width=True)
    st.plotly_chart(fig4_航運, use_container_width=True)

    # --- Balance Sheet Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_balance_sheet')}")
    st.dataframe(ranking_bal_航運, use_container_width=True)

with col2:
    st.subheader(get_text('income_statement_analysis'))
    st.markdown(f"#### {get_text('buffett_income_rule')}")
    st.caption(get_text('income_rule_desc'))

    results2_航運 = run_buffett_column2_analysis(df_original_航運.copy())

    df_wide_inc_航運 = results2_航運["df_wide"]
    df_top5_inc_航運 = results2_航運["df_top5_inc"]
    fig_inc_航運 = results2_航運["fig_income"]
    fig5_航運 = results2_航運["fig1_inc"]
    fig6_航運 = results2_航運["fig2_inc"]
    fig7_航運 = results2_航運["fig3_inc"]
    fig8_航運 = results2_航運["fig4_inc"]
    ranking_inc_航運 = results2_航運["ranking_inc"]

    st.plotly_chart(fig_inc_航運, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_income_statement')}")
    st.plotly_chart(fig5_航運, use_container_width=True)
    st.plotly_chart(fig6_航運, use_container_width=True)
    st.plotly_chart(fig7_航運, use_container_width=True)
    st.plotly_chart(fig8_航運, use_container_width=True)

    # --- Income Statement Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_income_statement')}")
    st.dataframe(ranking_inc_航運, use_container_width=True)

with col3:
    st.subheader(get_text('cash_flow_analysis'))
    st.markdown(f"#### {get_text('feroldi_cash_flow_rule')}")
    st.caption(get_text('cash_flow_rule_desc_detailed'))

    results3_航運 = run_cashflow_column3_analysis(df_original_航運.copy())

    df_wide_cash_航運 = results3_航運["df_wide"]
    df_top5_cash_航運 = results3_航運["df_top5"]
    fig_cash_航運 = results3_航運["fig_heatmap"]
    fig9_航運 = results3_航運["fig1"]
    fig10_航運 = results3_航運["fig2"]
    fig11_航運 = results3_航運["fig3"]
    fig12_航運 = results3_航運["fig4"]
    ranking_cash_航運 = results3_航運["ranking_df"]

    st.plotly_chart(fig_cash_航運, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_cash_flow')}")
    st.plotly_chart(fig9_航運, use_container_width=True)
    st.plotly_chart(fig10_航運, use_container_width=True)
    st.plotly_chart(fig11_航運, use_container_width=True)
    st.plotly_chart(fig12_航運, use_container_width=True)

    # --- Cash Flow Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_cash_flow')}")
    st.dataframe(ranking_cash_航運, use_container_width=True)

# --- Register rankings for Stock Agent ---
from finmind_tools import register_industry_rankings

register_industry_rankings(
    industry_name="航運業",
    bal_df=ranking_bal_航運,
    inc_df=ranking_inc_航運,
    cf_df=ranking_cash_航運
)