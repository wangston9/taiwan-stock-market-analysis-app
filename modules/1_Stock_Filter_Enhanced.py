import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import numpy as np
from datetime import datetime, timedelta

from dotenv import load_dotenv
from openai import OpenAI

from finmind_tools import (
    get_taiwan_stock_info,
    get_price_30days,
    get_api_usage,
    get_all_financials,
    get_stocks_by_industry,
    FINMIND_TOKEN
)
from language_config import get_text, get_current_language, is_all_value

# --- Load environment variable for OpenAI ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Enhanced CSS Styling ---
st.markdown("""
    <style>
    .filter-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stock-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .price-display {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .filter-header {
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .advanced-filter {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# --- Caching wrappers ---
@st.cache_data(ttl=86400)
def cached_stock_info():
    return get_taiwan_stock_info(FINMIND_TOKEN)

@st.cache_data(ttl=3600)
def cached_price(stock_id):
    return get_price_30days(stock_id, FINMIND_TOKEN)

@st.cache_data
def load_industry_options():
    df = get_taiwan_stock_info()
    if not df.empty and "industry_category" in df.columns:
        return sorted(df["industry_category"].dropna().unique().tolist())
    return []

# --- Enhanced filtering functions ---
def calculate_technical_indicators(df_price):
    """Calculate technical indicators for enhanced analysis"""
    if df_price.empty or len(df_price) < 5:
        return {}
    
    # Simple Moving Averages
    df_price['SMA_5'] = df_price['close'].rolling(window=5).mean()
    df_price['SMA_10'] = df_price['close'].rolling(window=10).mean()
    
    # RSI calculation
    delta = df_price['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    latest = df_price.iloc[-1]
    indicators = {
        'current_price': latest['close'],
        'volume': latest.get('Trading_Volume', 0),
        'sma_5': df_price['SMA_5'].iloc[-1] if not df_price['SMA_5'].isna().all() else 0,
        'sma_10': df_price['SMA_10'].iloc[-1] if not df_price['SMA_10'].isna().all() else 0,
        'rsi': rsi.iloc[-1] if not rsi.isna().all() else 50,
        'price_change_pct': ((latest['close'] - df_price['close'].iloc[0]) / df_price['close'].iloc[0]) * 100 if len(df_price) > 1 and df_price['close'].iloc[0] != 0 else 0
    }
    
    return indicators

def create_advanced_chart(df_price, stock_name, stock_id):
    """Create enhanced chart with technical indicators"""
    if df_price.empty:
        return None
    
    # Calculate indicators
    df_price['SMA_5'] = df_price['close'].rolling(window=5).mean()
    df_price['SMA_10'] = df_price['close'].rolling(window=10).mean()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=[f'{stock_name} ({stock_id}) - Price & Volume', 'Volume'],
        vertical_spacing=0.05
    )
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df_price["date"],
        open=df_price["open"],
        high=df_price["max"],
        low=df_price["min"],
        close=df_price["close"],
        name="Price",
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff3366'
    ), row=1, col=1)
    
    # Moving averages
    if not df_price['SMA_5'].isna().all():
        fig.add_trace(go.Scatter(
            x=df_price["date"],
            y=df_price['SMA_5'],
            name="SMA 5",
            line=dict(color='orange', width=2)
        ), row=1, col=1)
    
    if not df_price['SMA_10'].isna().all():
        fig.add_trace(go.Scatter(
            x=df_price["date"],
            y=df_price['SMA_10'],
            name="SMA 10",
            line=dict(color='purple', width=2)
        ), row=1, col=1)
    
    # Volume chart
    colors = ['#00ff88' if close >= open else '#ff3366' 
              for close, open in zip(df_price['close'], df_price['open'])]
    
    if 'Trading_Volume' in df_price.columns:
        fig.add_trace(go.Bar(
            x=df_price["date"],
            y=df_price['Trading_Volume'],
            name="Volume",
            marker_color=colors,
            opacity=0.7
        ), row=2, col=1)
    
    fig.update_layout(
        height=600,
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# --- Main Layout ---
st.markdown(f'<h1 style="text-align: center; color: #667eea; margin-bottom: 2rem;">{get_text("advanced_stock_filter_title")}</h1>', unsafe_allow_html=True)

# Initialize session state
all_text = get_text('all')
for key, default in {
    "selected_industry": all_text,
    "sort_by": "stock_id",
    "selected_stocks": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Load data
df_info = cached_stock_info()
if df_info.empty:
    st.error("❌ No stock data available")
    st.stop()

industry_options = load_industry_options()

# --- Simplified Filters ---
st.markdown(f"### {get_text('filter_options')}")

# Simple layout without styled containers
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    selected_industry = st.selectbox(
        get_text('select_industry'),
        [all_text] + industry_options,
        index=0
    )

with col2:
    sort_options = {
        "stock_id": get_text('sort_stock_id'), 
        "stock_name": get_text('sort_company_name'),
        "price": get_text('sort_price'),
        "price_change": get_text('sort_price_change')
    }
    sort_by = st.selectbox(
        get_text('sort_by'),
        list(sort_options.keys()),
        format_func=lambda x: sort_options[x]
    )
    st.session_state.sort_by = sort_by

with col3:
    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to align with selectboxes
    if st.button(get_text('reset_filter'), use_container_width=True):
        selected_industry = all_text
        st.rerun()

# --- Main Content Area ---
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    # Filter stocks based on criteria
    df_filtered = df_info.copy()
    
    if not is_all_value(selected_industry):
        df_filtered = df_filtered[df_filtered["industry_category"] == selected_industry]
    
    # Create stock cards with enhanced information
    st.markdown(f"### {get_text('filtered_stocks')}")
    
    if df_filtered.empty:
        st.warning(get_text('no_matching_criteria'))
    else:
        # Add technical analysis for each stock
        enhanced_stocks = []
        
        with st.spinner(get_text('analyzing_stocks')):
            for _, row in df_filtered.head(20).iterrows():  # Limit to 20 for performance
                stock_id = row["stock_id"]
                try:
                    df_price = cached_price(stock_id)
                    if not df_price.empty and len(df_price) > 0:
                        indicators = calculate_technical_indicators(df_price)
                        
                        # Only add stocks with valid price data
                        if indicators.get('current_price', 0) > 0:
                            enhanced_stock = {
                                'stock_id': stock_id,
                                'stock_name': row["stock_name"],
                                'industry': row["industry_category"],
                                **indicators
                            }
                            enhanced_stocks.append(enhanced_stock)
                except Exception as e:
                    # Skip stocks with data issues instead of adding empty entries
                    continue
        
        # Apply additional filters
        enhanced_df = pd.DataFrame(enhanced_stocks)
        if enhanced_df.empty:
            st.warning(get_text('no_valid_price_data'))
        else:
            # Only filter by industry (price and volume filters removed)
            pass
            
            # Sort results
            if st.session_state.sort_by == "price":
                enhanced_df = enhanced_df.sort_values('current_price', ascending=False)
            elif st.session_state.sort_by == "price_change":
                enhanced_df = enhanced_df.sort_values('price_change_pct', ascending=False)
            else:
                enhanced_df = enhanced_df.sort_values(st.session_state.sort_by)
            
            # Display stock cards
            for _, stock in enhanced_df.iterrows():
                with st.container():
                    # Handle infinite or invalid percentage values
                    price_change_pct = stock['price_change_pct']
                    if pd.isna(price_change_pct) or np.isinf(price_change_pct):
                        price_change_pct = 0
                        change_display = "N/A"
                    else:
                        change_display = f"{price_change_pct:+.2f}%"
                    
                    # Determine price change color (darker for better contrast on white background)
                    change_color = "#28a745" if price_change_pct > 0 else "#dc3545" if price_change_pct < 0 else "#6c757d"
                    arrow = "▲" if price_change_pct > 0 else "▼" if price_change_pct < 0 else "➖"
                    
                    # Handle price display
                    current_price = stock.get('current_price', 0)
                    if current_price <= 0:
                        continue  # Skip stocks with invalid prices
                    
                    st.markdown(f"""
                    <div class="stock-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin: 0; color: #2c3e50;">{stock['stock_id']} - {stock['stock_name']}</h4>
                                <p style="margin: 5px 0; color: #7f8c8d; font-size: 0.9em;">{stock['industry']}</p>
                                <small style="color: #999;">{get_text('volume_label')} {stock.get('volume', 0):,.0f}</small>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.2em; font-weight: bold; color: {change_color};">
                                    {arrow} {current_price:.2f} TWD
                                </div>
                                <div style="font-size: 0.9em; color: {change_color};">
                                    {change_display}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"{get_text('analyze_stock')} {stock['stock_id']}", key=f"analyze_{stock['stock_id']}", use_container_width=True):
                        st.session_state.selected_stock = stock['stock_id']

with col2:
    if 'selected_stock' in st.session_state and st.session_state.selected_stock:
        selected_id = st.session_state.selected_stock
        
        # Get stock details
        stock_row = df_info[df_info["stock_id"] == selected_id].iloc[0]
        df_price = cached_price(selected_id)
        
        if not df_price.empty:
            st.markdown(f"### {stock_row['stock_name']} ({selected_id})")
            
            # Price display
            latest_row = df_price.iloc[-1]
            latest_price = latest_row["close"]
            if len(df_price) > 1:
                price_change = latest_price - df_price.iloc[-2]["close"]
                change_pct = (price_change / df_price.iloc[-2]["close"]) * 100
                arrow = "▲" if price_change > 0 else "▼" if price_change < 0 else "➖"
                color = "#28a745" if price_change > 0 else "#dc3545" if price_change < 0 else "#6c757d"
            else:
                price_change, change_pct, arrow, color = 0, 0, "➖", "#888888"
            
            st.markdown(f"""
            <div class="price-display">
                <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">
                    {arrow} {latest_price:.2f} TWD
                </div>
                <div style="font-size: 1.2rem;">
                    {price_change:+.2f} ({change_pct:+.2f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced chart
            fig = create_advanced_chart(df_price, stock_row['stock_name'], selected_id)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # Technical indicators
            indicators = calculate_technical_indicators(df_price)
            if indicators:
                st.markdown(f"#### {get_text('technical_indicators')}")
                
                col_t1, col_t2, col_t3 = st.columns(3)
                
                with col_t1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4 style="color: #333333;">{get_text('rsi_label')}</h4>
                        <p style="font-size: 1.5rem; color: {'#ff3366' if indicators['rsi'] > 70 else '#00ff88' if indicators['rsi'] < 30 else '#667eea'};">
                            {indicators['rsi']:.1f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_t2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4 style="color: #333333;">{get_text('sma_5_label')}</h4>
                        <p style="font-size: 1.2rem; color: #667eea;">
                            {indicators['sma_5']:.2f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_t3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4 style="color: #333333;">{get_text('sma_10_label')}</h4>
                        <p style="font-size: 1.2rem; color: #667eea;">
                            {indicators['sma_10']:.2f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # AI Analysis
            st.markdown(f"#### {get_text('ai_business_description')}")
            company_name = stock_row["stock_name"]
            industry = stock_row.get("industry_category", "N/A")
            
            current_lang = get_current_language()
            if current_lang == 'zh':
                prompt = f"""
                分析台股公司'{company_name}'（代號{selected_id}）的投資價值。
                行業：{industry}
                目前股價：{latest_price:.2f} TWD
                近期漲跌：{change_pct:+.2f}%
                
                請提供：
                1. 公司業務簡介
                2. 技術面分析
                3. 投資建議
                
                請用繁體中文回答，保持專業但易懂。
                """
            else:
                prompt = f"""
                Analyze the investment potential of Taiwan stock '{company_name}' (ID: {selected_id}).
                Industry: {industry}
                Current Price: {latest_price:.2f} TWD
                Recent Change: {change_pct:+.2f}%
                
                Please provide:
                1. Company business overview
                2. Technical analysis
                3. Investment recommendation
                
                Keep it professional but accessible.
                """
            
            with st.spinner(get_text('ai_analyzing')):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a professional financial analyst."},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True
                    )
                    
                    analysis_text = ""
                    analysis_container = st.empty()
                    
                    for chunk in response:
                        content = chunk.choices[0].delta.content
                        if content:
                            analysis_text += content
                            analysis_container.markdown(f"""
                            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea; color: #333333;">
                                {analysis_text}
                            </div>
                            """, unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"AI Analysis unavailable: {str(e)}")
        
        else:
            st.warning(get_text('no_price_data_available'))
    
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 15px; margin-top: 2rem;">
            <h3 style="color: #667eea;">{get_text('select_stock_to_analyze')}</h3>
            <p style="color: #7f8c8d;">{get_text('choose_stock_message')}</p>
        </div>
        """, unsafe_allow_html=True)

# --- API Usage Display ---
st.markdown("---")
usage = get_api_usage(FINMIND_TOKEN)
st.info(f"{get_text('finmind_api_remaining')} {usage}")