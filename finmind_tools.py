# finmind_tools.py

import os
import pandas as pd
from typing import Dict
from dotenv import load_dotenv
from FinMind.data import DataLoader
import requests
from typing import Dict
import numpy as np
import plotly.express as px
from langchain.tools import tool

# --- Load Token ---
load_dotenv()
FINMIND_TOKEN = os.getenv("FINMIND_TOKEN")

if not FINMIND_TOKEN:
    raise ValueError("❌ FINMIND_TOKEN not found. Please add it to your .env file.")

# --- Initialize API ---
api = DataLoader()
api.login_by_token(api_token=FINMIND_TOKEN)

# --- FinMind Stock Info ---
def get_taiwan_stock_info(token=FINMIND_TOKEN):
    # Try API first
    url = "https://api.finmindtrade.com/api/v4/data"
    params = {"dataset": "TaiwanStockInfo", "token": token}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == 200:
            return pd.DataFrame(data["data"])
    except Exception as e:
        print(f"❌ Error fetching stock info: {e}")
    
    # Fallback: Extract stock info from local CSV files
    try:
        return get_stock_info_from_csv()
    except Exception as e:
        print(f"❌ Error fetching from CSV: {e}")
    return pd.DataFrame()

def get_stock_info_from_csv():
    """Fallback function to get stock info from local CSV files when API is exhausted"""
    import glob
    stock_info_list = []
    
    # Get all CSV files in finmind_data directory
    csv_files = glob.glob("finmind_data/*.csv")
    
    for csv_file in csv_files:
        try:
            # Extract industry name from filename
            industry_name = os.path.basename(csv_file).replace('.csv', '')
            
            # Read CSV and get unique stock info
            df = pd.read_csv(csv_file)
            if 'stock_id' in df.columns and 'stock_name' in df.columns:
                unique_stocks = df[['stock_id', 'stock_name']].drop_duplicates()
                unique_stocks['industry_category'] = industry_name
                stock_info_list.append(unique_stocks)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    
    if stock_info_list:
        combined_df = pd.concat(stock_info_list, ignore_index=True)
        return combined_df
    
    return pd.DataFrame()

# --- FinMind Price (Last 30 Days) ---
def get_price_30days(stock_id, token=FINMIND_TOKEN):
    url = "https://api.finmindtrade.com/api/v4/data"
    params = {
        "dataset": "TaiwanStockPrice",
        "data_id": stock_id,
        "start_date": (pd.Timestamp.now() - pd.Timedelta(days=30)).date().isoformat(),
        "token": token
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == 200 and data["data"]:
            df = pd.DataFrame(data["data"])
            return df.dropna(subset=["open", "max", "min", "close"])
    except Exception as e:
        print(f"❌ Error fetching price: {e}")
    return pd.DataFrame()

# --- API Usage ---
def get_api_usage(token=FINMIND_TOKEN):
    url = "https://api.web.finmindtrade.com/v2/user_info"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            used = data.get("user_count")
            limit = data.get("api_request_limit")
            if used is not None and limit is not None:
                return f"{limit - used} / {limit}"
        return "❓ Unknown"
    except Exception as e:
        return f"❌ Exception: {e}"

def get_api_quota_info(token=FINMIND_TOKEN):
    """Get detailed API quota information including reset time"""
    url = "https://api.web.finmindtrade.com/v2/user_info"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            used = data.get("user_count")
            limit = data.get("api_request_limit")
            
            if used is not None and limit is not None:
                remaining = limit - used
                
                # Calculate time until next hour (when quota resets)
                from datetime import datetime, timedelta
                now = datetime.now()
                next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                time_until_reset = next_hour - now
                
                minutes_remaining = int(time_until_reset.total_seconds() / 60)
                
                return {
                    "remaining": remaining,
                    "used": used,
                    "limit": limit,
                    "minutes_until_reset": minutes_remaining,
                    "is_exhausted": remaining <= 0
                }
        return None
    except Exception as e:
        print(f"Error fetching quota info: {e}")
        return None



# --- Tool for Stock Agent ---
# Internal memory store to hold ranking data for each industry
ranking_data_by_industry: Dict[str, Dict[str, pd.DataFrame]] = {}

def register_industry_rankings(industry_name: str, bal_df: pd.DataFrame, inc_df: pd.DataFrame, cf_df: pd.DataFrame):
    """
    Registers the ranking data for a given industry to be used later by the agent.
    """
    ranking_data_by_industry[industry_name] = {
        "balance": bal_df,
        "income": inc_df,
        "cashflow": cf_df
    }

def preload_all_industry_rankings():
    """
    Preloads ranking data for all industries by analyzing their CSV files.
    This ensures the Stock Agent has access to all industry data without needing
    users to visit each industry page first.
    """
    import glob
    
    # Get all CSV files in finmind_data directory
    csv_files = glob.glob("finmind_data/*.csv")
    
    for csv_file in csv_files:
        try:
            # Extract industry name from filename (e.g., "綠能環保類.csv" -> "綠能環保類")
            industry_name = os.path.basename(csv_file).replace('.csv', '')
            
            # Skip if already loaded
            if industry_name in ranking_data_by_industry:
                continue
                
            # Load and analyze the CSV file
            df_original = analyze_csv_to_wide_df(csv_file)
            
            # Run the three analysis pipelines
            results_bal = run_buffett_column1_analysis(df_original.copy())
            results_inc = run_buffett_column2_analysis(df_original.copy())  
            results_cf = run_cashflow_column3_analysis(df_original.copy())
            
            # Extract ranking DataFrames
            ranking_bal = results_bal["ranking_df"]
            ranking_inc = results_inc["ranking_inc"] 
            ranking_cf = results_cf["ranking_df"]
            
            # Register the rankings
            register_industry_rankings(industry_name, ranking_bal, ranking_inc, ranking_cf)
            
        except Exception as e:
            # Silently skip problematic files to avoid breaking the agent
            print(f"Warning: Could not preload {csv_file}: {e}")
            continue

def get_language_instruction():
    """Get language instruction for AI prompts based on current language setting"""
    from language_config import get_current_language
    
    current_lang = get_current_language()
    if current_lang == "zh":
        return "請用繁體中文回答。"
    else:
        return "Please respond in English."

def get_chart_titles():
    """Get chart titles based on current language setting"""
    from language_config import get_current_language
    
    current_lang = get_current_language()
    
    if current_lang == "zh":
        return {
            # Balance Sheet Charts
            'chart1_balance': '圖表1：現金佔總債務百分比（前5大股票）',
            'chart2_balance': '圖表2：負債權益比隨時間變化（前5大股票）', 
            'chart3_balance': '圖表3：保留盈餘成長（絕對值）',
            'chart4_balance': '圖表4：保留盈餘成長率（與4季前比較）',
            
            # Income Statement Charts
            'chart1_income': '圖表1：毛利率隨時間變化（前5大股票）',
            'chart2_income': '圖表2：淨利率隨時間變化（前5大股票）',
            'chart3_income': '圖表3：每股盈餘隨時間變化（前5大股票）',
            'chart4_income': '圖表4：營收成長率隨時間變化（前5大股票）',
            
            # Cash Flow Charts  
            'chart1_cashflow': '圖表1：自由現金流隨時間變化（前5大股票）',
            'chart2_cashflow': '圖表2：淨債務變化隨時間變化（前5大股票）',
            'chart3_cashflow': '圖表3：經營現金流隨時間變化（前5大股票）',
            'chart4_cashflow': '圖表4：資本支出隨時間變化（前5大股票）',
            'chart5_cashflow': '圖表5：債務發行隨時間變化（前5大股票）',
            'chart6_cashflow': '圖表6：債務償還隨時間變化（前5大股票）',
            
            # Axis Labels
            'date_label': '日期',
            'cash_debt_label': '現金/總債務百分比',
            'debt_equity_label': '負債權益比',
            'retained_earnings_label': '保留盈餘成長',
            'gross_margin_label': '毛利率',
            'net_margin_label': '淨利率', 
            'eps_label': '每股盈餘',
            'revenue_growth_label': '營收成長率',
            'free_cashflow_label': '自由現金流',
            'operating_cashflow_label': '經營現金流'
        }
    else:
        return {
            # Balance Sheet Charts
            'chart1_balance': 'Chart 1: % Cash over Total Debt (Top 5 Stocks)',
            'chart2_balance': 'Chart 2: Debt-to-Equity Ratio Over Time (Top 5 Stocks)',
            'chart3_balance': 'Chart 3: Retained Earnings Growth (Absolute)',
            'chart4_balance': 'Chart 4: % Retained Earnings Growth vs 4 Qtrs Ago',
            
            # Income Statement Charts
            'chart1_income': 'Chart 1: Gross Margin Over Time (Top 5 Stocks)',
            'chart2_income': 'Chart 2: Net Margin Over Time (Top 5 Stocks)', 
            'chart3_income': 'Chart 3: EPS Over Time (Top 5 Stocks)',
            'chart4_income': 'Chart 4: Revenue Growth Over Time (Top 5 Stocks)',
            
            # Cash Flow Charts
            'chart1_cashflow': 'Chart 1: Free Cash Flow Over Time (Top 5 Stocks)',
            'chart2_cashflow': 'Chart 2: Net Debt Change Over Time (Top 5 Stocks)',
            'chart3_cashflow': 'Chart 3: Operating Cash Flow Over Time (Top 5 Stocks)', 
            'chart4_cashflow': 'Chart 4: CapEx Over Time (Top 5 Stocks)',
            'chart5_cashflow': 'Chart 5: Debt Issued Over Time (Top 5 Stocks)',
            'chart6_cashflow': 'Chart 6: Debt Repaid Over Time (Top 5 Stocks)',
            
            # Axis Labels
            'date_label': 'Date',
            'cash_debt_label': '% Cash / Total Debt',
            'debt_equity_label': 'Debt-to-Equity Ratio',
            'retained_earnings_label': 'Retained Earnings Growth',
            'gross_margin_label': 'Gross Margin',
            'net_margin_label': 'Net Margin',
            'eps_label': 'Earnings Per Share',
            'revenue_growth_label': 'Revenue Growth Rate',
            'free_cashflow_label': 'Free Cash Flow',
            'operating_cashflow_label': 'Operating Cash Flow'
        }

@tool
def get_best_stock_for_industry(industry: str) -> str:
    """
    Determines the best stock for a given industry by analyzing balance sheet,
    income statement, and cash flow rankings. Passes real ranking tables for LLM evaluation.
    """
    data = ranking_data_by_industry.get(industry)
    if not data:
        # Try to preload all industry rankings if not already loaded
        try:
            preload_all_industry_rankings()
            data = ranking_data_by_industry.get(industry)
        except Exception as e:
            pass  # Silently continue if preload fails
            
    if not data:
        return f"❌ No ranking data found for '{industry}'. Available industries: {list(ranking_data_by_industry.keys())}"

    bal = data.get("balance")
    inc = data.get("income")
    cf = data.get("cashflow")

    if bal is None or inc is None or cf is None:
        return "⚠️ Incomplete ranking data."

    # Convert to Markdown so GPT can "read" it
    bal_md = bal.head(5).to_markdown(index=False)
    inc_md = inc.head(5).to_markdown(index=False)
    cf_md = cf.head(5).to_markdown(index=False)

    # Add language instruction
    language_instruction = get_language_instruction()
    
    prompt = f"""
Based on the following top 5 ranked stocks in the **{industry}** industry,
analyze which stock is the best overall choice and justify your answer.

### Balance Sheet Ranking
{bal_md}

### Income Statement Ranking
{inc_md}

### Cash Flow Ranking
{cf_md}

{language_instruction}
"""

    return prompt

# --- Get all 3 reports for a stock ---
def get_all_financials(stock_id: str, start_date: str = "2019-01-01") -> pd.DataFrame:
    try:
        fin = api.taiwan_stock_financial_statement(stock_id=stock_id, start_date=start_date)
        bal = api.taiwan_stock_balance_sheet(stock_id=stock_id, start_date=start_date)
        cash = api.taiwan_stock_cash_flows_statement(stock_id=stock_id, start_date=start_date)

        fin['report'] = 'IncomeStatement'
        bal['report'] = 'BalanceSheet'
        cash['report'] = 'CashFlow'

        df = pd.concat([fin, bal, cash], ignore_index=True)
        df['stock_id'] = stock_id
        return df
    except Exception as e:
        print(f"❌ Error fetching data for {stock_id}: {e}")
        return pd.DataFrame()

# --- Get all stock IDs by industry name ---
def get_stocks_by_industry(industry: str) -> pd.DataFrame:
    url = "https://api.finmindtrade.com/api/v4/data"
    params = {
        "dataset": "TaiwanStockInfo",
        "token": FINMIND_TOKEN
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json().get("data", [])
        df = pd.DataFrame(data)
        return df[df["industry_category"].str.contains(industry, na=False)]
    except Exception as e:
        print(f"❌ Error fetching industry stocks: {e}")
        return pd.DataFrame()



# --- Tool wrapper for LLM agent (LangChain use) ---
from langchain_core.tools import tool

@tool
def get_financial_statements(stock_id: str, start_date: str = "2019-01-01") -> str:
    """
    Fetches Taiwan financial statements for a stock ID and returns a summary of all available metrics.
    Displays both English code (type) and original Chinese name (origin_name).
    """
    df = get_financial_statements(stock_id, start_date)
    if df.empty:
        return f"No financial data found for {stock_id} since {start_date}."

    summary = ""
    for date in sorted(df["date"].unique(), reverse=True):
        sub = df[df["date"] == date]
        if sub.empty:
            continue

        summary += f"\n📅 Date: {date}\n"
        for _, row in sub.iterrows():
            try:
                value_fmt = f"{row['value']:.2f}" if isinstance(row['value'], (int, float)) else str(row['value'])
                summary += f"• {row['type']} ({row['origin_name']}): {value_fmt}\n"
            except:
                continue

    return summary if summary else "No recognized financial metrics found."


def analyze_csv_to_wide_df(csv_path: str) -> pd.DataFrame:
    """
    Loads a long-format financial CSV and pivots it to wide format, removing duplicate rows
    that only differ in 'industry' (e.g., '居家生活' vs '居家生活類').

    Parameters:
        csv_path (str): Path to the financial CSV file.

    Returns:
        df_wide (pd.DataFrame): Wide-format financial DataFrame.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ File not found: {csv_path}")

    # Step 1: Load and preprocess
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])

    # Step 2: Drop duplicate rows, allowing 'industry' to vary
    columns_except_industry = [col for col in df.columns if col != 'industry']
    df = df.drop_duplicates(subset=columns_except_industry)

    # Step 3: Pivot to wide format
    df_wide = df.pivot_table(
        index=['date', 'stock_id', 'stock_name', 'industry'],
        columns='type',
        values='value',
        aggfunc='first'
    ).reset_index()
    df_wide.columns.name = None

    return df_wide


# Tool for Column 1 for Balance_Sheet
def run_buffett_column1_analysis(df: pd.DataFrame) -> Dict[str, object]:
    """
    Runs full Buffett-style analysis pipeline used in Streamlit Column 1:
    - Applies Buffett rules
    - Adds % metrics
    - Filters date >= 2020
    - Prepares heatmap data and top 5 stock trends
    - Returns all data + plotly figures for rendering
    """

    # --- Step 1: Apply Buffett Rules ---
    df = df.copy()
    df = df.sort_values(by=['stock_id', 'date'])
    df['CashAndCashEquivalents'] = df['CashAndCashEquivalents'].fillna(0)
    df['ShorttermBorrowings'] = df['ShorttermBorrowings'].fillna(0)
    df['LongtermBorrowings'] = df['LongtermBorrowings'].fillna(0)
    df['Equity'] = df['Equity'].replace(0, pd.NA)

    df['TotalDebt'] = df['ShorttermBorrowings'] + df['LongtermBorrowings']
    df['HasMoreCashThanDebt'] = df['CashAndCashEquivalents'] > df['TotalDebt']
    df['DebtToEquity'] = df['TotalDebt'] / df['Equity']
    df['LowDebtToEquity'] = df['DebtToEquity'] < 0.8
    df['RetainedEarningsGrowth'] = df.groupby('stock_id')['RetainedEarnings'].diff(4)
    df['PositiveRetainedEarningsGrowth'] = df['RetainedEarningsGrowth'] > 0

    # Final Rule: Pass if all conditions met
    df['PassedAllBuffettRules'] = (
        df['HasMoreCashThanDebt'] &
        df['LowDebtToEquity'] &
        df['PositiveRetainedEarningsGrowth']
    )

    # --- Step 2: Add % Metrics ---
    df['CashOverDebt_Pct'] = (df['CashAndCashEquivalents'] / df['TotalDebt']) * 100
    df['CashOverDebt_Pct'] = df['CashOverDebt_Pct'].replace([np.inf, -np.inf], pd.NA)
    df.loc[df['TotalDebt'] == 0, 'CashOverDebt_Pct'] = 10000  # Special marker

    df['RetainedEarnings_4Q_Ago'] = df.groupby('stock_id')['RetainedEarnings'].shift(4)
    df['RetainedEarningsGrowth_Pct'] = (
        df['RetainedEarningsGrowth'] / df['RetainedEarnings_4Q_Ago']
    ) * 100
    df['RetainedEarningsGrowth_Pct'] = df['RetainedEarningsGrowth_Pct'].replace([np.inf, -np.inf], pd.NA)
    df.loc[
        (df['RetainedEarnings_4Q_Ago'] <= 0) |
        df['RetainedEarnings_4Q_Ago'].isna(),
        'RetainedEarningsGrowth_Pct'
    ] = pd.NA

    # --- Step 3: Filter data to >= 2020 ---
    df = df[df['date'] >= '2020-01-01'].copy()

    # --- Step 4: Heatmap Prep ---
    df['PassedInt'] = df['PassedAllBuffettRules'].astype(int)
    pass_rate_df = (
        df.groupby(['stock_id', 'stock_name'])['PassedInt']
        .agg(['sum', 'count']).reset_index()
    )
    pass_rate_df['PassRate'] = (pass_rate_df['sum'] / pass_rate_df['count']).round(2)
    pass_rate_df['stock_label'] = (
        pass_rate_df['stock_name'] + ' (' + pass_rate_df['stock_id'].astype(str) + ')  —  ' +
        (pass_rate_df['PassRate'] * 100).astype(int).astype(str) + '%'
    )

    heat_df = df.merge(pass_rate_df[['stock_id', 'stock_label', 'PassRate']], on='stock_id', how='left')
    # Remove duplicates before pivoting - keep first occurrence
    heat_df = heat_df.drop_duplicates(subset=['stock_label', 'date'], keep='first')
    heat_matrix = heat_df.pivot(index='stock_label', columns='date', values='PassedInt').fillna(0)
    sorted_labels = pass_rate_df.sort_values(by='PassRate', ascending=False)['stock_label']
    heat_matrix = heat_matrix.loc[sorted_labels]

    # --- Step 5: Top 5 Stock Trends ---
    top_5_ids = pass_rate_df.sort_values(by='PassRate', ascending=False).head(5)['stock_id'].tolist()
    top_5_names = pass_rate_df.set_index('stock_id')['stock_name'].to_dict()
    df_top5 = df[df['stock_id'].isin(top_5_ids)].copy()
    df_top5['stock_name'] = df_top5['stock_id'].map(top_5_names)

    # --- Step 6: Ranking Table ---
    ranking_df = df_top5.groupby(['stock_id', 'stock_name'])[
        ['CashOverDebt_Pct', 'DebtToEquity', 'RetainedEarningsGrowth_Pct']
    ].mean().reset_index()
    ranking_df = ranking_df.round(2).rename(columns={
        'CashOverDebt_Pct': 'Avg % Cash/Debt',
        'DebtToEquity': 'Avg Debt/Equity',
        'RetainedEarningsGrowth_Pct': 'Avg % Ret. Earnings Growth'
    })
    # Add % Passed column
    ranking_df = ranking_df.merge(pass_rate_df[['stock_id', 'PassRate']], on='stock_id', how='left')
    ranking_df['% Passed'] = (ranking_df['PassRate'] * 100).astype(int).astype(str) + '%'
    ranking_df = ranking_df.drop(columns='PassRate')
    ranking_df = ranking_df.sort_values(by='Avg % Cash/Debt', ascending=False).reset_index(drop=True)
    ranking_df = ranking_df[
    ['stock_id', 'stock_name', '% Passed',
     'Avg % Cash/Debt', 'Avg Debt/Equity', 'Avg % Ret. Earnings Growth']
]
    # --- Step 7: Plotly Charts ---
    fig_heat = px.imshow(
        heat_matrix,
        color_continuous_scale=[[0.0, "#ffffff"], [1.0, "#006400"]],
        zmin=0, zmax=1,
        aspect='auto'
    )
    fig_heat.update_coloraxes(showscale=False)
    fig_heat.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock + % Passed",
        height=800,
        template="plotly_white"
    )

    # Get language-aware chart titles
    titles = get_chart_titles()
    
    fig1 = px.line(
        df_top5, x='date', y='CashOverDebt_Pct', color='stock_name',
        title=titles['chart1_balance'],
        labels={'CashOverDebt_Pct': titles['cash_debt_label'], 'date': titles['date_label']}
    )
    fig1.update_layout(template='plotly_white')

    fig2 = px.line(
        df_top5, x='date', y='DebtToEquity', color='stock_name',
        title=titles['chart2_balance'],
        labels={'DebtToEquity': titles['debt_equity_label'], 'date': titles['date_label']}
    )
    fig2.add_hline(y=0.8, line_dash="dash", line_color="red", annotation_text="Threshold: < 0.8")
    fig2.update_layout(template='plotly_white')

    fig3 = px.line(
        df_top5, x='date', y='RetainedEarningsGrowth', color='stock_name',
        title=titles['chart3_balance'],
        labels={'RetainedEarningsGrowth': titles['retained_earnings_label'], 'date': titles['date_label']}
    )
    fig3.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Threshold: > 0")
    fig3.update_layout(template='plotly_white')

    fig4 = px.line(
        df_top5, x='date', y='RetainedEarningsGrowth_Pct', color='stock_name',
        title=titles['chart4_balance'],
        labels={'RetainedEarningsGrowth_Pct': titles['retained_earnings_label'], 'date': titles['date_label']}
    )
    fig4.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Threshold: > 0")
    fig4.update_layout(template='plotly_white')

    return {
        "df_wide": df,
        "df_top5": df_top5,
        "ranking_df": ranking_df,
        "fig_heatmap": fig_heat,
        "fig1": fig1,
        "fig2": fig2,
        "fig3": fig3,
        "fig4": fig4
    }

# Tool for Column 2 for Income_Statement
def run_buffett_column2_analysis(df: pd.DataFrame) -> dict:
    """
    Applies Buffett-style income statement rules to a wide-format DataFrame.
    Returns charts and rankings for Streamlit Column 2.

    Rules:
    - Gross Margin > 30%
    - Interest Expense Margin < 25%
    - Net Profit Margin > 5%
    - EPS positive and YoY growth
    """
    import plotly.express as px
    import pandas as pd
    import numpy as np

    df = df.copy()
    df = df.sort_values(by=['stock_id', 'date'])

    # --- Clean required columns ---
    for col in ['GrossProfit', 'Revenue', 'InterestExpense', 'OperatingIncome', 'TAX',
                'PreTaxIncome', 'IncomeAfterTaxes', 'EPS']:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    df['PreTaxIncome'] = df['PreTaxIncome'].replace(0, pd.NA)

    # --- Rule 1: Gross Margin > 30%
    df['GrossMargin'] = df['GrossProfit'] / df['Revenue']
    df['PassedGrossMargin'] = df['GrossMargin'] > 0.30

    # --- Rule 4: Interest Expense Margin < 25%
    df['InterestMargin'] = df['InterestExpense'] / df['OperatingIncome']
    df['PassedInterestMargin'] = df['InterestMargin'] < 0.25

    # --- Rule 6: Net Profit Margin > 5%
    df['NetProfitMargin'] = df['IncomeAfterTaxes'] / df['Revenue']
    df['PassedNetMargin'] = df['NetProfitMargin'] > 0.05

    # --- Rule 7: EPS positive and growing YoY
    df['EPS_Growth_4Q'] = df.groupby('stock_id')['EPS'].diff(4)
    df['EPS_4Q_Ago'] = df.groupby('stock_id')['EPS'].shift(4)
    df['PassedEPS'] = (
        (df['EPS'] > 0) &
        (df['EPS_4Q_Ago'].notna()) &
        (df['EPS'] >= df['EPS_4Q_Ago'])
    )

    # --- Final Pass Flag ---
    df['PassedAllBuffettIncomeRules'] = (
        df['PassedGrossMargin'] &
        df['PassedInterestMargin'] &
        df['PassedNetMargin'] &
        df['PassedEPS']
    )

    # Step 3: Filter data to >= 2020
    df = df[df['date'] >= '2020-01-01'].copy()

    # Step 4: Heatmap Prep (mirroring Column 1 style)
    df['PassedInt'] = df['PassedAllBuffettIncomeRules'].astype(int)

    pass_rate_df = (
        df.groupby(['stock_id', 'stock_name'])['PassedInt']
        .agg(['sum', 'count']).reset_index()
    )
    pass_rate_df['PassRate'] = (pass_rate_df['sum'] / pass_rate_df['count']).round(2)
    pass_rate_df['stock_label'] = (
        pass_rate_df['stock_name'] + ' (' + pass_rate_df['stock_id'].astype(str) + ')  —  ' +
        (pass_rate_df['PassRate'] * 100).astype(int).astype(str) + '%'
    )

    heat_df = df.merge(pass_rate_df[['stock_id', 'stock_label', 'PassRate']], on='stock_id', how='left')
    # Remove duplicates before pivoting - keep first occurrence
    heat_df = heat_df.drop_duplicates(subset=['stock_label', 'date'], keep='first')
    heat_matrix = heat_df.pivot(index='stock_label', columns='date', values='PassedInt').fillna(0)
    sorted_labels = pass_rate_df.sort_values(by='PassRate', ascending=False)['stock_label']
    heat_matrix = heat_matrix.loc[sorted_labels]

    fig_income = px.imshow(
        heat_matrix,
        color_continuous_scale=[[0.0, "#ffffff"], [1.0, "#006400"]],
        zmin=0, zmax=1,
        aspect='auto'
    )
    fig_income.update_coloraxes(showscale=False)
    fig_income.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock + % Passed",
        height=800,
        template="plotly_white"
    )

    # --- Top 5 Trend Charts ---
    top_ids = pass_rate_df.sort_values(by='PassRate', ascending=False).head(5)['stock_id'].tolist()
    top_names = pass_rate_df.set_index('stock_id')['stock_name'].to_dict()
    df_top5 = df[df['stock_id'].isin(top_ids)].copy()
    df_top5['stock_name'] = df_top5['stock_id'].map(top_names)

    # Get language-aware chart titles
    titles = get_chart_titles()
    
    fig1 = px.line(df_top5, x='date', y='GrossMargin', color='stock_name', title=titles['chart1_income'])
    fig2 = px.line(df_top5, x='date', y='InterestMargin', color='stock_name', title=titles['chart2_income'])
    fig3 = px.line(df_top5, x='date', y='NetProfitMargin', color='stock_name', title=titles['chart3_income'])
    fig4 = px.line(df_top5, x='date', y='EPS', color='stock_name', title=titles['chart4_income'])

    # Add threshold lines
    fig1.add_hline(y=0.30, line_dash="dash", line_color="red", annotation_text="Threshold: > 30%")
    fig2.add_hline(y=0.25, line_dash="dash", line_color="red", annotation_text="Threshold: < 25%")
    fig3.add_hline(y=0.05, line_dash="dash", line_color="red", annotation_text="Threshold: > 5%")
    fig4.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Threshold: EPS > 0 & ↑")

    # --- Ranking Table ---
# --- Ranking Table (Colab-style) ---
    df_top5['InterestMargin'] = df_top5['InterestMargin'].replace([np.inf, -np.inf], np.nan)

    ranking_df = df_top5.groupby(['stock_id', 'stock_name'])[
        ['GrossMargin', 'InterestMargin', 'NetProfitMargin', 'EPS']
    ].mean().reset_index()

    # Convert to %
    ranking_df['GrossMargin'] = (ranking_df['GrossMargin'] * 100).round(2)
    ranking_df['InterestMargin'] = (ranking_df['InterestMargin'] * 100).round(2)
    ranking_df['NetProfitMargin'] = (ranking_df['NetProfitMargin'] * 100).round(2)
    ranking_df['EPS'] = ranking_df['EPS'].round(2)

    # Rename
    ranking_df = ranking_df.rename(columns={
        'GrossMargin': 'Avg Gross Margin (%)',
        'InterestMargin': 'Avg Interest Margin (%)',
        'NetProfitMargin': 'Avg Net Profit Margin (%)',
        'EPS': 'Avg EPS'
    })

    # Add % Passed column
    ranking_df = ranking_df.merge(pass_rate_df[['stock_id', 'PassRate']], on='stock_id', how='left')
    ranking_df['% Passed'] = (ranking_df['PassRate'] * 100).astype(int).astype(str) + '%'
    ranking_df = ranking_df.drop(columns='PassRate')

    # Reorder
    ranking_df = ranking_df[
        ['stock_id', 'stock_name', '% Passed',
        'Avg Gross Margin (%)', 'Avg Interest Margin (%)',
        'Avg Net Profit Margin (%)', 'Avg EPS']
]

    return {
        "df_wide": df, 
        "fig_income": fig_income,
        "df_top5_inc": df_top5,
        "ranking_inc": ranking_df,
        "fig_income": fig_income,
        "fig1_inc": fig1,
        "fig2_inc": fig2,
        "fig3_inc": fig3,
        "fig4_inc": fig4
    }

#Tool for Column 3 for Cashflow
def run_cashflow_column3_analysis(df: pd.DataFrame) -> dict:
    import plotly.express as px
    import pandas as pd

    df = df.copy()
    df = df.sort_values(by=['stock_id', 'date'])

    # --- Fill required columns ---
    for col in ['CashFlowsFromOperatingActivities', 'PropertyAndPlantAndEquipment',
                'ProceedsFromLongTermDebt', 'RepaymentOfLongTermDebt']:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # --- Compute derived metrics ---
    df['FreeCashFlow'] = df['CashFlowsFromOperatingActivities'] - abs(df['PropertyAndPlantAndEquipment'])
    df['DebtIssued'] = df['ProceedsFromLongTermDebt']
    df['DebtRepaid'] = df['RepaymentOfLongTermDebt']
    df['NetDebtChange'] = df['DebtIssued'] - df['DebtRepaid']

    # --- Feroldi 4-point test (strict)
    df['Passed'] = (
        (df['CashFlowsFromOperatingActivities'] > 0) &
        (df['FreeCashFlow'] > 0) &
        (df['NetDebtChange'] <= 0) &
        (abs(df['PropertyAndPlantAndEquipment']) < df['CashFlowsFromOperatingActivities'])
    )

    df = df[df['date'] >= '2020-01-01'].copy()
    df['PassedInt'] = df['Passed'].astype(int)

    # --- Heatmap ---
    pass_rate_df = (
        df.groupby(['stock_id', 'stock_name'])['PassedInt']
        .agg(['sum', 'count']).reset_index()
    )
    pass_rate_df['PassRate'] = (pass_rate_df['sum'] / pass_rate_df['count']).round(2)
    pass_rate_df['stock_label'] = (
        pass_rate_df['stock_name'] + ' (' + pass_rate_df['stock_id'].astype(str) + ')  —  ' +
        (pass_rate_df['PassRate'] * 100).astype(int).astype(str) + '%'
    )

    heat_df = df.merge(pass_rate_df[['stock_id', 'stock_label', 'PassRate']], on='stock_id', how='left')
    # Remove duplicates before pivoting - keep first occurrence
    heat_df = heat_df.drop_duplicates(subset=['stock_label', 'date'], keep='first')
    heat_matrix = heat_df.pivot(index='stock_label', columns='date', values='PassedInt').fillna(0)
    sorted_labels = pass_rate_df.sort_values(by='PassRate', ascending=False)['stock_label']
    heat_matrix = heat_matrix.loc[sorted_labels]

    fig_heat = px.imshow(
        heat_matrix,
        color_continuous_scale=[[0.0, "#ffffff"], [1.0, "#006400"]],
        zmin=0, zmax=1,
        aspect='auto'
    )
    fig_heat.update_coloraxes(showscale=False)
    fig_heat.update_layout(
        xaxis_title="Date",
        yaxis_title="Stock + % Passed",
        height=800,
        template="plotly_white"
    )

    # --- Top 5 Stocks ---
    top_ids = pass_rate_df.sort_values(by='PassRate', ascending=False).head(5)['stock_id'].tolist()
    top_names = pass_rate_df.set_index('stock_id')['stock_name'].to_dict()
    df_top5 = df[df['stock_id'].isin(top_ids)].copy()
    df_top5['stock_name'] = df_top5['stock_id'].map(top_names)

    # --- Trend Charts ---
    # Get language-aware chart titles
    titles = get_chart_titles()
    
    fig1 = px.line(df_top5, x='date', y='FreeCashFlow', color='stock_name', title=titles['chart1_cashflow'])
    fig2 = px.line(df_top5, x='date', y='NetDebtChange', color='stock_name', title=titles['chart2_cashflow'])
    fig3 = px.line(df_top5, x='date', y='CashFlowsFromOperatingActivities', color='stock_name', title=titles['chart3_cashflow'])
    fig4 = px.line(df_top5, x='date', y='PropertyAndPlantAndEquipment', color='stock_name', title=titles['chart4_cashflow'])
    fig5 = px.line(df_top5, x='date', y='DebtIssued', color='stock_name', title=titles['chart5_cashflow'])
    fig6 = px.line(df_top5, x='date', y='DebtRepaid', color='stock_name', title=titles['chart6_cashflow'])

    # --- Ranking Table ---
    ranking_df = df_top5.groupby(['stock_id', 'stock_name'])[
        ['FreeCashFlow', 'NetDebtChange']
    ].mean().reset_index().round(2)

    ranking_df = ranking_df.rename(columns={
        'FreeCashFlow': 'Avg Free Cash Flow',
        'NetDebtChange': 'Avg Net Debt Change'
    })
    # Add % Passed column
    ranking_df = ranking_df.merge(pass_rate_df[['stock_id', 'PassRate']], on='stock_id', how='left')
    ranking_df['% Passed'] = (ranking_df['PassRate'] * 100).astype(int).astype(str) + '%'
    ranking_df = ranking_df.drop(columns='PassRate')
    ranking_df = ranking_df.sort_values(by='Avg Free Cash Flow', ascending=False).reset_index(drop=True)
    ranking_df = ranking_df[
    ['stock_id', 'stock_name', '% Passed',
     'Avg Free Cash Flow', 'Avg Net Debt Change']
]
    return {
        "df_wide": df,
        "df_top5": df_top5,
        "fig_heatmap": fig_heat,
        "fig1": fig1,
        "fig2": fig2,
        "fig3": fig3,
        "fig4": fig4,
        "fig5": fig5,
        "fig6": fig6,
        "ranking_df": ranking_df
    }
