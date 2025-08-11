# Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
import os
from finmind_tools import get_api_quota_info
from language_config import get_text, create_language_selector, create_sidebar_navigation

# Set page config with default title (will be overridden by sidebar)
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Sidebar navigation (includes language selector)
create_sidebar_navigation("dashboard")

# Custom CSS for better styling and contrast
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    color: #2C3E50;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.metric-card {
    background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.metric-card h3 {
    color: #ECF0F1 !important;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.metric-card h2 {
    color: #FFFFFF !important;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0.5rem 0;
}
.metric-card p {
    color: #E8F4FD !important;
    font-size: 0.9rem;
    font-weight: 500;
}
.industry-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #D5D8DC;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}
.industry-card h4 {
    color: #2C3E50 !important;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.industry-card p {
    color: #5D6D7E !important;
}
.quick-nav {
    background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem;
    color: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.quick-nav h3 {
    color: #FFFFFF !important;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.quick-nav p {
    color: #E8F4FD !important;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown(f'<h1 class="main-header">{get_text("dashboard_title")}</h1>', unsafe_allow_html=True)

# --- Market Overview Section ---
st.markdown(f"## {get_text('market_overview')}")

# Industry name mapping function
def get_translated_industry_name(chinese_name):
    """Map Chinese CSV filename to translated industry name"""
    industry_mapping = {
        '食品工業': 'food_industry',
        '居家生活': 'home_living', 
        '半導體業': 'semiconductor',
        '電子商務業': 'ecommerce',
        '農業科技': 'agri_tech',
        '玻璃陶瓷': 'glass_ceramics',
        '水泥工業': 'cement',
        '造紙工業': 'paper',
        '運動休閒類': 'sports_leisure',
        '橡膠工業': 'rubber',
        '油電燃氣業': 'oil_gas',
        '綠能環保類': 'green_energy',
        '塑膠工業': 'plastics',
        '航運業': 'shipping',
        '文化創意業': 'cultural_creative',
        '農業科技業': 'agri_tech_business',
        '觀光事業': 'tourism',
        '貿易百貨': 'trading_retail',
        '光電業': 'optoelectronics',
        '生技醫療業': 'biotechnology_medical',
        # Additional industries that might exist
        '金融業': 'financial_services',
        '受益證券': 'beneficiary_securities',
        '大盤': 'broad_market'
    }
    
    if chinese_name in industry_mapping:
        return get_text(industry_mapping[chinese_name])
    else:
        # Fallback to original name if no mapping found
        return chinese_name

# Load all industry data (no caching to ensure fresh count)
def load_all_industries_data():
    """Load data from all industry CSV files"""
    industries_data = {}
    csv_files = glob.glob("finmind_data/*.csv")
    
    total_stocks = 0
    total_companies = set()
    
    for csv_file in csv_files:
        try:
            industry_name = os.path.basename(csv_file).replace('.csv', '')
            df = pd.read_csv(csv_file)
            
            if not df.empty and 'stock_id' in df.columns:
                # Get unique companies
                unique_companies = df['stock_id'].nunique()
                company_names = df[['stock_id', 'stock_name']].drop_duplicates()
                total_companies.update(df['stock_id'].unique())
                
                # Get latest data
                if 'date' in df.columns:
                    latest_date = df['date'].max()
                    latest_data = df[df['date'] == latest_date]
                else:
                    latest_data = df
                
                industries_data[industry_name] = {
                    'total_companies': unique_companies,
                    'latest_data': latest_data,
                    'company_names': company_names
                }
                
        except Exception as e:
            st.error(f"Error loading {csv_file}: {e}")
    
    return industries_data, len(total_companies)

industries_data, total_unique_companies = load_all_industries_data()

# Top metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{get_text('industries')}</h3>
        <h2>{len(industries_data)}</h2>
        <p>{get_text('market_sectors')}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{get_text('companies')}</h3>
        <h2>{total_unique_companies}</h2>
        <p>{get_text('listed_stocks')}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    try:
        quota_info = get_api_quota_info()
        if quota_info:
            remaining = quota_info["remaining"]
            # Use darker colors for better contrast
            if remaining <= 0:
                bg_color = "linear-gradient(135deg, #C0392B 0%, #A93226 100%)"
            else:
                bg_color = "linear-gradient(135deg, #27AE60 0%, #229954 100%)"
            st.markdown(f"""
            <div class="metric-card" style="background: {bg_color};">
                <h3>{get_text('api_status')}</h3>
                <h2>{remaining}</h2>
                <p>{get_text('calls_remaining')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{get_text('api_status')}</h3>
                <h2>--</h2>
                <p>{get_text('unknown')}</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{get_text('api_status')}</h3>
            <h2>--</h2>
            <p>{get_text('offline')}</p>
        </div>
        """, unsafe_allow_html=True)

with col4:
    # Calculate actual date range from data
    try:
        # Get date range from a sample of the data
        sample_csv = next(iter(industries_data.values()))['latest_data'] if industries_data else None
        if sample_csv is not None and 'date' in sample_csv.columns:
            # Get the actual date range from all CSV files
            all_dates = []
            for csv_file in glob.glob("finmind_data/*.csv"):
                try:
                    df = pd.read_csv(csv_file, usecols=['date'], nrows=1000)  # Sample for performance
                    all_dates.extend(df['date'].tolist())
                except:
                    continue
            
            if all_dates:
                min_date = min(all_dates)
                max_date = max(all_dates)
                # Format as "Mar 2019 - Mar 2025"
                min_formatted = pd.to_datetime(min_date).strftime("%b %Y")
                max_formatted = pd.to_datetime(max_date).strftime("%b %Y")
                date_range = f"{min_formatted} - {max_formatted}"
            else:
                date_range = "Mar 2019 - Mar 2025"
        else:
            date_range = "Mar 2019 - Mar 2025"
    except:
        date_range = "Mar 2019 - Mar 2025"
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>{get_text('data_period')}</h3>
        <h2>{date_range}</h2>
        <p>{get_text('six_years_coverage')}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Industry Overview Charts ---
st.markdown(f"### {get_text('market_structure_rankings')}")

# First row: Company distribution
col1, col2 = st.columns([1, 1.4])

with col1:
    st.markdown(f"#### {get_text('industries_by_company_count')}")
    if industries_data:
        # Create industry size chart
        industry_sizes = []
        for industry, data in industries_data.items():
            industry_sizes.append({
                'Industry': get_translated_industry_name(industry),
                'Companies': data['total_companies']
            })
        
        size_df = pd.DataFrame(industry_sizes).sort_values('Companies', ascending=True)
        
        fig_bar = px.bar(
            size_df, 
            x='Companies', 
            y='Industry',
            orientation='h',
            color='Companies',
            color_continuous_scale='blues',
            title=get_text('companies_per_industry')
        )
        fig_bar.update_layout(
            height=600,  # Increased height to accommodate all industry names
            showlegend=False,
            title_font_size=14,
            font=dict(size=11),
            margin=dict(l=120, r=20, t=40, b=20),  # More left margin for industry names
            yaxis=dict(tickfont=dict(size=11))  # Larger font for Chinese industry names
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown(f"#### {get_text('market_distribution')}")
    if industries_data:
        # Create pie chart
        fig_pie = px.pie(
            size_df,
            values='Companies',
            names='Industry',
            title=get_text('market_share_by_industry'),
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(
            textposition='outside', 
            textinfo='percent+label',
            textfont_size=9,  # Smaller font to fit more labels
            pull=[0.05 if x == size_df['Companies'].max() else 0 for x in size_df['Companies']],
            hovertemplate='<b>%{label}</b><br>' +
                         'Companies: %{value}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>'
        )
        fig_pie.update_layout(
            height=650,  # Increased height for better spacing
            title_font_size=14,
            font=dict(size=9),
            showlegend=False,
            margin=dict(t=80, b=150, l=120, r=120),  # Much larger margins for leader lines
            annotations=[
                dict(text='', x=0.5, y=-0.1, xref='paper', yref='paper', 
                     showarrow=False, font=dict(size=8))
            ]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# Second row: Financial Analysis Rankings
st.markdown("---")

def calculate_industry_rankings():
    """Calculate average pass rates for each industry across all analysis types"""
    industry_rankings = {}
    
    for csv_file in glob.glob("finmind_data/*.csv"):
        try:
            industry_name = os.path.basename(csv_file).replace('.csv', '')
            df = pd.read_csv(csv_file)
            
            if df.empty or 'date' not in df.columns:
                continue
                
            # Filter to recent data (2020+) like in the analysis modules
            df = df[df['date'] >= '2020-01-01'].copy()
            
            if df.empty:
                continue
            
            # Calculate metrics for each analysis type
            rankings = {}
            
            # Balance Sheet Analysis (simplified)
            try:
                balance_data = df[df['type'].isin(['CashAndCashEquivalents', 'TotalLiabilities', 'RetainedEarnings', 'TotalCurrentLiabilities'])].copy()
                if not balance_data.empty:
                    # Simple balance sheet health check
                    cash_avg = balance_data[balance_data['type'] == 'CashAndCashEquivalents']['value'].mean() if not balance_data[balance_data['type'] == 'CashAndCashEquivalents'].empty else 0
                    debt_avg = balance_data[balance_data['type'].isin(['TotalLiabilities', 'TotalCurrentLiabilities'])]['value'].mean() if not balance_data[balance_data['type'].isin(['TotalLiabilities', 'TotalCurrentLiabilities'])].empty else 0
                    retained_avg = balance_data[balance_data['type'] == 'RetainedEarnings']['value'].mean() if not balance_data[balance_data['type'] == 'RetainedEarnings'].empty else 0
                    rankings['Balance Sheet'] = max(0, (cash_avg + retained_avg - debt_avg) / 1000000)  # Simplified score
            except:
                rankings['Balance Sheet'] = 0
            
            # Income Statement Analysis (simplified)  
            try:
                income_data = df[df['type'].isin(['Revenue', 'NetIncome', 'IncomeBeforeIncomeTax', 'GrossProfit'])].copy()
                if not income_data.empty:
                    revenue_avg = income_data[income_data['type'] == 'Revenue']['value'].mean() if not income_data[income_data['type'] == 'Revenue'].empty else 0
                    profit_avg = income_data[income_data['type'] == 'NetIncome']['value'].mean() if not income_data[income_data['type'] == 'NetIncome'].empty else 0
                    gross_profit_avg = income_data[income_data['type'] == 'GrossProfit']['value'].mean() if not income_data[income_data['type'] == 'GrossProfit'].empty else 0
                    # Calculate profitability score - use absolute value to show performance magnitude
                    if profit_avg != 0:
                        rankings['Income Statement'] = abs(profit_avg) / 1000000
                    elif gross_profit_avg != 0:
                        rankings['Income Statement'] = abs(gross_profit_avg) / 1000000  
                    else:
                        rankings['Income Statement'] = 0
            except:
                rankings['Income Statement'] = 0
            
            # Cash Flow Analysis (simplified)
            try:
                cf_data = df[df['type'] == 'CashFlowsFromOperatingActivities'].copy()
                if not cf_data.empty:
                    cf_avg = cf_data['value'].mean()
                    rankings['Cash Flow'] = max(0, cf_avg) / 1000000  # Simplified score
                else:
                    rankings['Cash Flow'] = 0
            except:
                rankings['Cash Flow'] = 0
            
            industry_rankings[industry_name] = rankings
            
        except Exception as e:
            continue
    
    return industry_rankings

# Calculate rankings
industry_rankings = calculate_industry_rankings()

if industry_rankings:
    # Create three ranking charts
    col1, col2, col3 = st.columns(3)
    
    analysis_types = ['Balance Sheet', 'Income Statement', 'Cash Flow']
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    
    for i, (analysis_type, color) in enumerate(zip(analysis_types, colors)):
        # Prepare data for this analysis type
        ranking_data = []
        for industry, scores in industry_rankings.items():
            score = scores.get(analysis_type, 0)
            ranking_data.append({
                'Industry': get_translated_industry_name(industry),
                'Score': score
            })
        
        rank_df = pd.DataFrame(ranking_data).sort_values('Score', ascending=True)
        
        # Create chart
        fig = px.bar(
            rank_df,  # Show all industries
            x='Score',
            y='Industry',
            orientation='h',
            title=get_text(f"{analysis_type.lower().replace(' ', '_')}_strength"),
            color_discrete_sequence=[color]
        )
        # Add unit descriptions for each analysis type
        if analysis_type == "Balance Sheet":
            x_title = get_text('balance_sheet_desc')
        elif analysis_type == "Income Statement":
            x_title = get_text('income_statement_desc')
        else:  # Cash Flow
            x_title = get_text('cash_flow_desc')
            
        fig.update_layout(
            height=500,
            title_font_size=14,
            font=dict(size=9),
            showlegend=False,
            xaxis_title=x_title,
            yaxis_title=""
        )
        
        with [col1, col2, col3][i]:
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Quick actions are now available in the left sidebar for easy navigation

