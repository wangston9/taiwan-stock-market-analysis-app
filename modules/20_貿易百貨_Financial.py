# modules/25_貿易百貨_Financial.py

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
    df_original_貿易百貨 = analyze_csv_to_wide_df("finmind_data/貿易百貨.csv")
    if df_original_貿易百貨.empty:
        st.error("❌ 貿易百貨 data is empty")
        st.stop()
except FileNotFoundError as e:
    st.error(f"❌ File not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading 貿易百貨 data: {e}")
    st.stop()

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(get_text('balance_sheet_analysis'))
    st.markdown(f"#### {get_text('buffett_balance_sheet_rule')}")
    st.caption(get_text('balance_sheet_rule_desc'))

    try:
        results_貿易百貨 = run_buffett_column1_analysis(df_original_貿易百貨.copy())
        
        df_wide_bal_貿易百貨 = results_貿易百貨["df_wide"]
        df_top5_bal_貿易百貨 = results_貿易百貨["df_top5"] 
        fig_bal_貿易百貨 = results_貿易百貨["fig_heatmap"]
        fig1_貿易百貨 = results_貿易百貨["fig1"]
        fig2_貿易百貨 = results_貿易百貨["fig2"]
        fig3_貿易百貨 = results_貿易百貨["fig3"]
        fig4_貿易百貨 = results_貿易百貨["fig4"]
        ranking_bal_貿易百貨 = results_貿易百貨["ranking_df"]
    except Exception as e:
        st.error(f"❌ Error in balance sheet analysis: {e}")
        st.stop()

    st.plotly_chart(fig_bal_貿易百貨, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_balance_sheet')}")
    st.plotly_chart(fig1_貿易百貨, use_container_width=True)
    st.plotly_chart(fig2_貿易百貨, use_container_width=True)
    st.plotly_chart(fig3_貿易百貨, use_container_width=True)
    st.plotly_chart(fig4_貿易百貨, use_container_width=True)

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_balance_sheet')}")
    st.dataframe(ranking_bal_貿易百貨, use_container_width=True)

with col2:
    st.subheader(get_text('income_statement_analysis'))
    st.markdown(f"#### {get_text('buffett_income_statement_rule')}")
    st.caption(get_text('income_statement_rule_desc'))

    try:
        results2_貿易百貨 = run_buffett_column2_analysis(df_original_貿易百貨.copy())

        df_wide_inc_貿易百貨 = results2_貿易百貨["df_wide"]
        df_top5_inc_貿易百貨 = results2_貿易百貨["df_top5_inc"]
        fig_inc_貿易百貨 = results2_貿易百貨["fig_income"]
        fig5_貿易百貨 = results2_貿易百貨["fig1_inc"]
        fig6_貿易百貨 = results2_貿易百貨["fig2_inc"]
        fig7_貿易百貨 = results2_貿易百貨["fig3_inc"]
        fig8_貿易百貨 = results2_貿易百貨["fig4_inc"]
        ranking_inc_貿易百貨 = results2_貿易百貨["ranking_inc"]
    except Exception as e:
        st.error(f"❌ Error in income statement analysis: {e}")
        st.stop()

    st.plotly_chart(fig_inc_貿易百貨, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_income_statement')}")
    st.plotly_chart(fig5_貿易百貨, use_container_width=True)
    st.plotly_chart(fig6_貿易百貨, use_container_width=True)
    st.plotly_chart(fig7_貿易百貨, use_container_width=True)
    st.plotly_chart(fig8_貿易百貨, use_container_width=True)

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_income_statement')}")
    st.dataframe(ranking_inc_貿易百貨, use_container_width=True)

with col3:
    st.subheader(get_text('cash_flow_analysis'))
    st.markdown(f"#### {get_text('feroldi_cash_flow_rule')}")
    st.caption(get_text('cash_flow_rule_desc'))

    try:
        results3_貿易百貨 = run_cashflow_column3_analysis(df_original_貿易百貨.copy())

        df_wide_cf_貿易百貨 = results3_貿易百貨["df_wide"]
        df_top5_cf_貿易百貨 = results3_貿易百貨["df_top5"]
        fig_cf_貿易百貨 = results3_貿易百貨["fig_heatmap"]
        fig9_貿易百貨 = results3_貿易百貨["fig1"]
        fig10_貿易百貨 = results3_貿易百貨["fig2"]
        fig11_貿易百貨 = results3_貿易百貨["fig3"]
        fig12_貿易百貨 = results3_貿易百貨["fig4"]
        fig13_貿易百貨 = results3_貿易百貨["fig5"]
        fig14_貿易百貨 = results3_貿易百貨["fig6"]
        ranking_cf_貿易百貨 = results3_貿易百貨["ranking_df"]
    except Exception as e:
        st.error(f"❌ Error in cash flow analysis: {e}")
        st.stop()

    st.plotly_chart(fig_cf_貿易百貨, use_container_width=True)

    # --- Trend Charts ---
    st.markdown(f"#### {get_text('trend_charts_cash_flow')}")
    st.plotly_chart(fig9_貿易百貨, use_container_width=True)   # Free Cash Flow
    st.plotly_chart(fig10_貿易百貨, use_container_width=True)  # Net Debt Change
    st.plotly_chart(fig11_貿易百貨, use_container_width=True)  # Operating Cash Flow
    st.plotly_chart(fig12_貿易百貨, use_container_width=True)  # CapEx
    st.plotly_chart(fig13_貿易百貨, use_container_width=True)  # Debt Issued
    st.plotly_chart(fig14_貿易百貨, use_container_width=True)  # Debt Repaid

    # --- Ranking Table ---
    st.markdown(f"#### {get_text('ranked_metrics_top5_cash_flow')}")
    st.dataframe(ranking_cf_貿易百貨, use_container_width=True)

from finmind_tools import register_industry_rankings

register_industry_rankings(
    industry_name="貿易百貨",
    bal_df=ranking_bal_貿易百貨,
    inc_df=ranking_inc_貿易百貨,
    cf_df=ranking_cf_貿易百貨
)