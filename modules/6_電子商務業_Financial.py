# modules/9_電子商務業_Financial.py

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
    df_wide_電子商務業 = analyze_csv_to_wide_df("finmind_data/電子商務業.csv")
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

df_original_電子商務業 = analyze_csv_to_wide_df("finmind_data/電子商務業.csv")

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(get_text('balance_sheet_analysis'))
    st.markdown(f"#### {get_text('buffett_balance_sheet_rule')}")
    st.caption(get_text('balance_sheet_rule_desc'))

    results_電子商務業 = run_buffett_column1_analysis(df_original_電子商務業.copy())

    df_wide_bal_電子商務業 = results_電子商務業["df_wide"]
    df_top5_bal_電子商務業 = results_電子商務業["df_top5"]
    fig_bal_電子商務業 = results_電子商務業["fig_heatmap"]
    fig1_電子商務業 = results_電子商務業["fig1"]
    fig2_電子商務業 = results_電子商務業["fig2"]
    fig3_電子商務業 = results_電子商務業["fig3"]
    fig4_電子商務業 = results_電子商務業["fig4"]
    ranking_bal_電子商務業 = results_電子商務業["ranking_df"]

    st.plotly_chart(fig_bal_電子商務業, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_balance_sheet')}")
    st.plotly_chart(fig1_電子商務業, use_container_width=True)
    st.plotly_chart(fig2_電子商務業, use_container_width=True)
    st.plotly_chart(fig3_電子商務業, use_container_width=True)
    st.plotly_chart(fig4_電子商務業, use_container_width=True)

    # --- Balance Sheet Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_balance_sheet')}")
    st.dataframe(ranking_bal_電子商務業, use_container_width=True)

with col2:
    st.subheader(get_text('income_statement_analysis'))
    st.markdown(f"#### {get_text('buffett_income_rule')}")
    st.caption(get_text('income_rule_desc'))

    results2_電子商務業 = run_buffett_column2_analysis(df_original_電子商務業.copy())

    df_wide_inc_電子商務業 = results2_電子商務業["df_wide"]
    df_top5_inc_電子商務業 = results2_電子商務業["df_top5_inc"]
    fig_inc_電子商務業 = results2_電子商務業["fig_income"]
    fig5_電子商務業 = results2_電子商務業["fig1_inc"]
    fig6_電子商務業 = results2_電子商務業["fig2_inc"]
    fig7_電子商務業 = results2_電子商務業["fig3_inc"]
    fig8_電子商務業 = results2_電子商務業["fig4_inc"]
    ranking_inc_電子商務業 = results2_電子商務業["ranking_inc"]

    st.plotly_chart(fig_inc_電子商務業, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_income_statement')}")
    st.plotly_chart(fig5_電子商務業, use_container_width=True)
    st.plotly_chart(fig6_電子商務業, use_container_width=True)
    st.plotly_chart(fig7_電子商務業, use_container_width=True)
    st.plotly_chart(fig8_電子商務業, use_container_width=True)

    # --- Income Statement Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_income_statement')}")
    st.dataframe(ranking_inc_電子商務業, use_container_width=True)

with col3:
    st.subheader(get_text('cash_flow_analysis'))
    st.markdown(f"#### {get_text('feroldi_cash_flow_rule')}")
    st.caption(get_text('cash_flow_rule_desc_detailed'))

    results3_電子商務業 = run_cashflow_column3_analysis(df_original_電子商務業.copy())

    df_wide_cash_電子商務業 = results3_電子商務業["df_wide"]
    df_top5_cash_電子商務業 = results3_電子商務業["df_top5"]
    fig_cash_電子商務業 = results3_電子商務業["fig_heatmap"]
    fig9_電子商務業 = results3_電子商務業["fig1"]
    fig10_電子商務業 = results3_電子商務業["fig2"]
    fig11_電子商務業 = results3_電子商務業["fig3"]
    fig12_電子商務業 = results3_電子商務業["fig4"]
    ranking_cash_電子商務業 = results3_電子商務業["ranking_df"]

    st.plotly_chart(fig_cash_電子商務業, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_cash_flow')}")
    st.plotly_chart(fig9_電子商務業, use_container_width=True)
    st.plotly_chart(fig10_電子商務業, use_container_width=True)
    st.plotly_chart(fig11_電子商務業, use_container_width=True)
    st.plotly_chart(fig12_電子商務業, use_container_width=True)

    # --- Cash Flow Rankings ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_cash_flow')}")
    st.dataframe(ranking_cash_電子商務業, use_container_width=True)

# --- Register rankings for Stock Agent ---
from finmind_tools import register_industry_rankings

register_industry_rankings(
    industry_name="電子商務業",
    bal_df=ranking_bal_電子商務業,
    inc_df=ranking_inc_電子商務業,
    cf_df=ranking_cash_電子商務業
)