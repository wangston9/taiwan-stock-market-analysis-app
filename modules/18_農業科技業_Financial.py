# modules/23_農業科技業_Financial.py

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
    df_wide_農業科技業 = analyze_csv_to_wide_df("finmind_data/農業科技業.csv")
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

df_original_農業科技業 = analyze_csv_to_wide_df("finmind_data/農業科技業.csv")

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(get_text('balance_sheet_analysis'))
    st.markdown(f"#### {get_text('buffett_balance_sheet_rule')}")
    st.caption(get_text('balance_sheet_rule_desc'))

    try:
        results_農業科技業 = run_buffett_column1_analysis(df_original_農業科技業.copy())

        df_wide_bal_農業科技業 = results_農業科技業.get("df_wide", pd.DataFrame())
        df_top5_bal_農業科技業 = results_農業科技業.get("df_top5", pd.DataFrame())
        fig_bal_農業科技業 = results_農業科技業.get("fig_heatmap", None)
        fig1_農業科技業 = results_農業科技業.get("fig1", None)
        fig2_農業科技業 = results_農業科技業.get("fig2", None)
        fig3_農業科技業 = results_農業科技業.get("fig3", None)
        fig4_農業科技業 = results_農業科技業.get("fig4", None)
        ranking_bal_農業科技業 = results_農業科技業.get("ranking_df", pd.DataFrame())
    except Exception as e:
        st.error(f"Balance Sheet Analysis Error: {e}")
        fig_bal_農業科技業 = fig1_農業科技業 = fig2_農業科技業 = fig3_農業科技業 = fig4_農業科技業 = None
        ranking_bal_農業科技業 = pd.DataFrame()

    if fig_bal_農業科技業:
        st.plotly_chart(fig_bal_農業科技業, use_container_width=True)
    else:
        st.info("Balance sheet heatmap not available for this industry")

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_balance_sheet')}")
    if fig1_農業科技業:
        st.plotly_chart(fig1_農業科技業, use_container_width=True)
    if fig2_農業科技業:
        st.plotly_chart(fig2_農業科技業, use_container_width=True)
    if fig3_農業科技業:
        st.plotly_chart(fig3_農業科技業, use_container_width=True)
    if fig4_農業科技業:
        st.plotly_chart(fig4_農業科技業, use_container_width=True)
    
    if not any([fig1_農業科技業, fig2_農業科技業, fig3_農業科技業, fig4_農業科技業]):
        st.info("Trend charts not available - insufficient data for analysis")

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_balance_sheet')}")
    if not ranking_bal_農業科技業.empty:
        st.dataframe(ranking_bal_農業科技業, use_container_width=True)
    else:
        st.info("Ranking data not available for this industry")

with col2:
    st.subheader(get_text('income_statement_analysis'))
    st.markdown(f"#### {get_text('buffett_income_rule')}")
    st.caption(get_text('income_rule_desc'))

    try:
        results_income_農業科技業 = run_buffett_column2_analysis(df_original_農業科技業.copy())

        df_wide_inc_農業科技業 = results_income_農業科技業.get("df_wide", pd.DataFrame())
        df_top5_inc_農業科技業 = results_income_農業科技業.get("df_top5_inc", pd.DataFrame())
        fig_inc_農業科技業 = results_income_農業科技業.get("fig_income", None)
        fig5_農業科技業 = results_income_農業科技業.get("fig1_inc", None)
        fig6_農業科技業 = results_income_農業科技業.get("fig2_inc", None)
        fig7_農業科技業 = results_income_農業科技業.get("fig3_inc", None)
        fig8_農業科技業 = results_income_農業科技業.get("fig4_inc", None)
        ranking_inc_農業科技業 = results_income_農業科技業.get("ranking_inc", pd.DataFrame())
    except Exception as e:
        st.error(f"Income Statement Analysis Error: {e}")
        fig_inc_農業科技業 = fig5_農業科技業 = fig6_農業科技業 = fig7_農業科技業 = fig8_農業科技業 = None
        ranking_inc_農業科技業 = pd.DataFrame()

    if fig_inc_農業科技業:
        st.plotly_chart(fig_inc_農業科技業, use_container_width=True)
    else:
        st.info("Income statement heatmap not available for this industry")

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_income_statement')}")
    if fig5_農業科技業:
        st.plotly_chart(fig5_農業科技業, use_container_width=True)
    if fig6_農業科技業:
        st.plotly_chart(fig6_農業科技業, use_container_width=True)
    if fig7_農業科技業:
        st.plotly_chart(fig7_農業科技業, use_container_width=True)
    if fig8_農業科技業:
        st.plotly_chart(fig8_農業科技業, use_container_width=True)
    
    if not any([fig5_農業科技業, fig6_農業科技業, fig7_農業科技業, fig8_農業科技業]):
        st.info("Trend charts not available - insufficient data for analysis")

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_income_statement')}")
    if not ranking_inc_農業科技業.empty:
        st.dataframe(ranking_inc_農業科技業, use_container_width=True)
    else:
        st.info("Ranking data not available for this industry")

with col3:
    st.subheader(get_text('cash_flow_analysis'))
    st.markdown(f"#### {get_text('feroldi_cash_flow_rule')}")
    st.caption(get_text('cash_flow_rule_desc_detailed'))

    try:
        results_cf_農業科技業 = run_cashflow_column3_analysis(df_original_農業科技業.copy())

        df_wide_cf_農業科技業 = results_cf_農業科技業.get("df_wide", pd.DataFrame())
        df_top5_cf_農業科技業 = results_cf_農業科技業.get("df_top5", pd.DataFrame())
        fig_cf_農業科技業 = results_cf_農業科技業.get("fig_heatmap", None)
        fig9_農業科技業 = results_cf_農業科技業.get("fig1", None)
        fig10_農業科技業 = results_cf_農業科技業.get("fig2", None)
        fig11_農業科技業 = results_cf_農業科技業.get("fig3", None)
        fig12_農業科技業 = results_cf_農業科技業.get("fig4", None)
        ranking_cf_農業科技業 = results_cf_農業科技業.get("ranking_df", pd.DataFrame())
    except Exception as e:
        st.error(f"Cash Flow Analysis Error: {e}")
        fig_cf_農業科技業 = fig9_農業科技業 = fig10_農業科技業 = fig11_農業科技業 = fig12_農業科技業 = None
        ranking_cf_農業科技業 = pd.DataFrame()

    if fig_cf_農業科技業:
        st.plotly_chart(fig_cf_農業科技業, use_container_width=True)
    else:
        st.info("Cash flow heatmap not available for this industry")

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_cash_flow')}")
    if fig9_農業科技業:
        st.plotly_chart(fig9_農業科技業, use_container_width=True)
    if fig10_農業科技業:
        st.plotly_chart(fig10_農業科技業, use_container_width=True)
    if fig11_農業科技業:
        st.plotly_chart(fig11_農業科技業, use_container_width=True)
    if fig12_農業科技業:
        st.plotly_chart(fig12_農業科技業, use_container_width=True)
    
    if not any([fig9_農業科技業, fig10_農業科技業, fig11_農業科技業, fig12_農業科技業]):
        st.info("Trend charts not available - insufficient data for analysis")

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_cash_flow')}")
    if not ranking_cf_農業科技業.empty:
        st.dataframe(ranking_cf_農業科技業, use_container_width=True)
    else:
        st.info("Ranking data not available for this industry")

# Register the industry rankings for the Stock Agent
from finmind_tools import register_industry_rankings
register_industry_rankings(
    industry_name="農業科技業",
    bal_df=ranking_bal_農業科技業,
    inc_df=ranking_inc_農業科技業,
    cf_df=ranking_cf_農業科技業
)

