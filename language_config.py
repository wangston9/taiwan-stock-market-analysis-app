# language_config.py

import streamlit as st

# Language definitions
LANGUAGES = {
    "en": {
        "name": "English",
        "flag": "🇺🇸"
    },
    "zh": {
        "name": "繁體中文", 
        "flag": "assets/taiwan_flag.png"
    }
}

# Text translations
TRANSLATIONS = {
    # Dashboard texts
    "dashboard_title": {
        "en": "Taiwan Stock Market Dashboard",
        "zh": "台灣股市儀表板"
    },
    "market_overview": {
        "en": "Market Overview",
        "zh": "市場概覽"
    },
    "industries": {
        "en": "Industries",
        "zh": "行業"
    },
    "market_sectors": {
        "en": "Market Sectors",
        "zh": "市場板塊"
    },
    "companies": {
        "en": "Companies",
        "zh": "公司"
    },
    "listed_stocks": {
        "en": "Listed Stocks",
        "zh": "上市股票"
    },
    "api_status": {
        "en": "FinMind API Status",
        "zh": "FinMind API狀態"
    },
    "calls_remaining": {
        "en": "Calls Remaining",
        "zh": "剩餘調用次數"
    },
    "data_period": {
        "en": "Data Period",
        "zh": "資料期間"
    },
    "years_coverage": {
        "en": "Years Coverage",
        "zh": "年度覆蓋"
    },
    "market_structure_rankings": {
        "en": "Market Structure & Financial Rankings",
        "zh": "市場結構與財務排名"
    },
    "industries_by_company_count": {
        "en": "Industries by Company Count",
        "zh": "按公司數量分類的行業"
    },
    "companies_per_industry": {
        "en": "Companies per Industry",
        "zh": "每個行業的公司數量"
    },
    "market_distribution": {
        "en": "Market Distribution",
        "zh": "市場分佈"
    },
    "market_share_by_industry": {
        "en": "Market Share by Industry",
        "zh": "按行業劃分的市場份額"
    },
    "balance_sheet_strength": {
        "en": "Balance Sheet Strength",
        "zh": "資產負債表實力"
    },
    "income_statement_strength": {
        "en": "Income Statement Strength",
        "zh": "損益表實力"
    },
    "cash_flow_strength": {
        "en": "Cash Flow Strength",
        "zh": "現金流實力"
    },
    "balance_sheet_desc": {
        "en": "Average Net Worth<br>(Avg Cash + Avg Retained Earnings - Avg Debt, in Million TWD)",
        "zh": "平均淨資產<br>(平均現金 + 平均保留盈餘 - 平均負債，百萬新台幣)"
    },
    "income_statement_desc": {
        "en": "Average Profitability<br>(Avg Net Income, in Million TWD)",
        "zh": "平均獲利能力<br>(平均淨利，百萬新台幣)"
    },
    "cash_flow_desc": {
        "en": "Average Cash Flow<br>(Avg Operating Cash Flow, in Million TWD)",
        "zh": "平均現金流<br>(平均營運現金流，百萬新台幣)"
    },
    "balance_sheet_strength": {
        "en": "Balance Sheet Strength",
        "zh": "資產負債表實力"
    },
    "income_statement_strength": {
        "en": "Income Statement Strength", 
        "zh": "損益表實力"
    },
    "cash_flow_strength": {
        "en": "Cash Flow Strength",
        "zh": "現金流實力"
    },
    "quick_actions": {
        "en": "Quick Actions",
        "zh": "快捷操作"
    },
    "industry_analysis": {
        "en": "Industry Analysis",
        "zh": "行業分析"
    },
    "industry_analysis_desc": {
        "en": "Deep dive into sector performance with Buffett-style analysis",
        "zh": "使用巴菲特式分析深入了解行業表現"
    },
    "explore_industries": {
        "en": "Explore Industries",
        "zh": "探索行業"
    },
    "ai_stock_agent": {
        "en": "AI Stock Agent",
        "zh": "AI股票智能助手"
    },
    "ai_stock_agent_desc": {
        "en": "Get personalized stock recommendations powered by GPT",
        "zh": "獲取由GPT驅動的個人化股票推薦"
    },
    "ask_ai_agent": {
        "en": "Ask AI Agent",
        "zh": "詢問AI助手"
    },
    "stock_filter": {
        "en": "Stock Filter",
        "zh": "股票篩選器"
    },
    "stock_filter_desc": {
        "en": "Find stocks based on custom financial criteria",
        "zh": "根據自定義財務標準查找股票"
    },
    "filter_stocks": {
        "en": "Filter Stocks",
        "zh": "篩選股票"
    },
    
    # Stock Filter texts
    "taiwan_stock_dashboard": {
        "en": "Taiwan Stock Dashboard",
        "zh": "台灣股票儀表板"
    },
    "download_financial_data": {
        "en": "Download Financial Data by Industry",
        "zh": "按行業下載財務資料"
    },
    "select_industry": {
        "en": "Select Industry",
        "zh": "選擇行業"
    },
    "download": {
        "en": "Download",
        "zh": "下載"
    },
    "fetching_saving_data": {
        "en": "Fetching and saving financial data...",
        "zh": "正在獲取並保存財務資料..."
    },
    "no_stocks_found": {
        "en": "❌ No stocks found in this industry.",
        "zh": "❌ 在此行業中未找到股票。"
    },
    "no_financial_data": {
        "en": "⚠️ No financial data retrieved.",
        "zh": "⚠️ 未獲取到財務資料。"
    },
    "saved_to": {
        "en": "✅ Saved to",
        "zh": "✅ 已保存到"
    },
    "api_usage_remaining": {
        "en": "📶 API Usage Remaining:",
        "zh": "📶 API使用量剩餘："
    },
    "no_stock_info": {
        "en": "⚠️ No stock info available.",
        "zh": "⚠️ 無股票資訊可用。"
    },
    "filter_stocks_title": {
        "en": "🔎 Filter Stocks",
        "zh": "🔎 篩選股票"
    },
    "reset": {
        "en": "🔁 Reset",
        "zh": "🔁 重置"
    },
    "industry": {
        "en": "🏭 Industry",
        "zh": "🏭 行業"
    },
    "matching_stocks": {
        "en": "📋 Matching Stocks",
        "zh": "📋 匹配的股票"
    },
    "select_company": {
        "en": "▶️ Select a company",
        "zh": "▶️ 選擇一家公司"
    },
    "price_candlestick_chart": {
        "en": "📊 Price Candlestick Chart (Past 30 Days)",
        "zh": "📊 價格K線圖（過去30天）"
    },
    "ai_business_description": {
        "en": "🧠 AI Business Description",
        "zh": "🧠 AI企業描述"
    },
    "gpt_analyzing": {
        "en": "🤖 GPT is analyzing the company...",
        "zh": "🤖 GPT正在分析該公司..."
    },
    "no_price_data": {
        "en": "No price data found for this stock.",
        "zh": "未找到該股票的價格數據。"
    },
    "select_stock_prompt": {
        "en": "Select a Stock ID from Column 1 to see details here.",
        "zh": "從第1欄選擇股票代碼以在此查看詳細信息。"
    },
    
    # Navigation texts
    "navigation_guide": {
        "en": "Navigation Guide:",
        "zh": "導航指南："
    },
    "stock_filter_nav": {
        "en": "Stock Filter - Find stocks based on custom financial criteria",
        "zh": "股票篩選器 - 根據自定義財務標準查找股票"
    },
    "stock_agent_nav": {
        "en": "Stock Agent - Get AI-powered stock recommendations using GPT",
        "zh": "股票智能助手 - 使用GPT獲取AI驅動的股票推薦"
    },
    "industry_tabs_nav": {
        "en": "Industry Tabs - Deep dive into specific sector analysis with Buffett-style metrics",
        "zh": "行業標籤 - 使用巴菲特式指標深入分析特定行業"
    },
    
    # Industry Analysis Texts
    "balance_sheet_analysis": {
        "en": "📊 Balance Sheet Analysis",
        "zh": "📊 資產負債表分析"
    },
    "buffett_balance_sheet_rule": {
        "en": "Buffett Balance Sheet Rule Heatmap — Pass/Fail",
        "zh": "巴菲特資產負債表規則熱力圖 — 通過/失敗"
    },
    "balance_sheet_rule_desc": {
        "en": "✅ Pass if: Cash > Total Debt, Debt-to-Equity < 0.8, Retained Earnings are growing (YoY)",
        "zh": "✅ 通過條件：現金 > 總債務，負債權益比 < 0.8，保留盈餘年增長"
    },
    "trend_charts_balance_sheet": {
        "en": "📈 Trend Charts for Top 5 Balance Sheet Stocks",
        "zh": "📈 前5名資產負債表股票趨勢圖"
    },
    "income_statement_analysis": {
        "en": "📋 Income Statement Analysis",
        "zh": "📋 損益表分析"
    },
    "buffett_income_statement_rule": {
        "en": "Buffett Income Statement Rule Heatmap — Pass/Fail",
        "zh": "巴菲特損益表規則熱力圖 — 通過/失敗"
    },
    "income_statement_rule_desc": {
        "en": "✅ Pass if: ROE > 15%, ROA > 7%, Profit Margin > 10%, Revenue Growth > 5%",
        "zh": "✅ 通過條件：ROE > 15%，ROA > 7%，利潤率 > 10%，營收增長 > 5%"
    },
    "trend_charts_income_statement": {
        "en": "📈 Trend Charts for Top 5 Income Statement Stocks",
        "zh": "📈 前5名損益表股票趨勢圖"
    },
    "cash_flow_analysis": {
        "en": "💰 Cash Flow Analysis",
        "zh": "💰 現金流分析"
    },
    "buffett_cash_flow_rule": {
        "en": "Buffett Cash Flow Rule Heatmap — Pass/Fail",
        "zh": "巴菲特現金流規則熱力圖 — 通過/失敗"
    },
    "cash_flow_rule_desc": {
        "en": "✅ Pass if: Operating Cash Flow > 0, Free Cash Flow > 0, Cash Flow Growth > 0%",
        "zh": "✅ 通過條件：營運現金流 > 0，自由現金流 > 0，現金流增長 > 0%"
    },
    "trend_charts_cash_flow": {
        "en": "📈 Trend Charts for Top 5 Cash Flow Stocks",
        "zh": "📈 前5名現金流股票趨勢圖"
    },
    "top_stocks_ranking": {
        "en": "🏆 Top Stocks Ranking",
        "zh": "🏆 頂級股票排名"
    },
    
    # General
    "all": {
        "en": "All",
        "zh": "全部"
    },
    "unknown": {
        "en": "Unknown",
        "zh": "未知"
    },
    "offline": {
        "en": "Offline",
        "zh": "離線"
    },
    
    # Industry names
    "food_industry": {
        "en": "Food Industry",
        "zh": "食品工業"
    },
    "home_living": {
        "en": "Home & Living",
        "zh": "居家生活"
    },
    "semiconductor": {
        "en": "Semiconductor",
        "zh": "半導體業"
    },
    "ecommerce": {
        "en": "E-commerce",
        "zh": "電子商務業"
    },
    "agri_tech": {
        "en": "Agricultural Technology",
        "zh": "農業科技"
    },
    "glass_ceramics": {
        "en": "Glass & Ceramics",
        "zh": "玻璃陶瓷"
    },
    "cement": {
        "en": "Cement Industry",
        "zh": "水泥工業"
    },
    "paper": {
        "en": "Paper Industry",
        "zh": "造紙工業"
    },
    "sports_leisure": {
        "en": "Sports & Leisure",
        "zh": "運動休閒類"
    },
    "rubber": {
        "en": "Rubber Industry",
        "zh": "橡膠工業"
    },
    "oil_gas": {
        "en": "Oil, Gas & Utilities",
        "zh": "油電燃氣業"
    },
    "green_energy": {
        "en": "Green Energy",
        "zh": "綠能環保類"
    },
    "plastics": {
        "en": "Plastics Industry",
        "zh": "塑膠工業"
    },
    "shipping": {
        "en": "Shipping Industry",
        "zh": "航運業"
    },
    "cultural_creative": {
        "en": "Cultural & Creative",
        "zh": "文化創意業"
    },
    "agri_tech_business": {
        "en": "Agricultural Technology Business",
        "zh": "農業科技業"
    },
    "tourism": {
        "en": "Tourism Industry",
        "zh": "觀光事業"
    },
    "trading_retail": {
        "en": "Trading & Department Stores",
        "zh": "貿易百貨"
    },
    "optoelectronics": {
        "en": "Optoelectronics Industry",
        "zh": "光電業"
    },
    "biotechnology_medical": {
        "en": "Biotechnology & Medical Industry",
        "zh": "生技醫療業"
    },
    
    # Numbers and text combinations  
    "six_years_coverage": {
        "en": "6 Years Coverage",
        "zh": "6年覆蓋"
    },
    
    # Additional industries
    "financial_services": {
        "en": "Financial Services",
        "zh": "金融業"
    },
    "beneficiary_securities": {
        "en": "Beneficiary Securities", 
        "zh": "受益證券"
    },
    "broad_market": {
        "en": "Broad Market",
        "zh": "大盤"
    },
    
    # Industry analysis additional text
    "ranked_metrics_top5_balance_sheet": {
        "en": "🏆 Ranked Metrics: Top 5 Balance Sheet Companies",
        "zh": "🏆 排名指標：前5名資產負債表公司"
    },
    "buffett_income_rule": {
        "en": "Buffett Income Rule Heatmap — Pass/Fail",
        "zh": "巴菲特收益規則熱力圖 — 通過/失敗"
    },
    "income_rule_desc": {
        "en": "✅ Pass if: Gross Margin > 30%, Interest Margin < 25%, Net Profit Margin > 5%, EPS ↑ and > 0",
        "zh": "✅ 通過條件：毛利率 > 30%，利息毛利率 < 25%，淨利率 > 5%，每股盈餘 ↑ 且 > 0"
    },
    "ranked_metrics_top5_income_statement": {
        "en": "🏆 Ranked Metrics: Top 5 Income Statement Companies", 
        "zh": "🏆 排名指標：前5名損益表公司"
    },
    "feroldi_cash_flow_rule": {
        "en": "Feroldi-Style Cash Flow Heatmap — Pass/Fail",
        "zh": "費羅迪風格現金流熱力圖 — 通過/失敗"
    },
    "cash_flow_rule_desc_detailed": {
        "en": "✅ Pass if: Operating CF > 0, Free CF > 0, Net Debt Change ≤ 0, CapEx < Operating CF",
        "zh": "✅ 通過條件：營運現金流 > 0，自由現金流 > 0，淨債務變化 ≤ 0，資本支出 < 營運現金流"
    },
    "ranked_metrics_top5_cash_flow": {
        "en": "🏆 Ranked Metrics: Top 5 Cash Flow Companies",
        "zh": "🏆 排名指標：前5名現金流公司"
    },
    
    # Navigation and UI elements
    "language_selector": {
        "en": "Language",
        "zh": "語言"
    },
    "navigation": {
        "en": "Navigation",
        "zh": "導航"
    },
    "stock_analysis_sections": {
        "en": "Stock Analysis Sections",
        "zh": "股票分析部分"
    },
    "industries_section": {
        "en": "Industries",
        "zh": "行業"
    },
    "select_industry": {
        "en": "Select Industry:",
        "zh": "選擇行業："
    },
    "select_analysis_section": {
        "en": "Select Analysis Section:",
        "zh": "選擇分析部分："
    },
    "error_loading_module": {
        "en": "Error loading",
        "zh": "載入錯誤"
    },
    "error_loading_file": {
        "en": "Error loading",
        "zh": "載入錯誤"
    },
    "date_range_fallback": {
        "en": "Mar 2019 - Mar 2025",
        "zh": "2019年3月 - 2025年3月"
    },
    
    # Stock Filter Enhanced translations
    "advanced_stock_filter_title": {
        "en": "Advanced Stock Filter & Analysis",
        "zh": "高級股票篩選器與分析"
    },
    "filter_options": {
        "en": "Filter Options",
        "zh": "篩選選項"
    },
    "filtered_stocks": {
        "en": "Filtered Stocks",
        "zh": "篩選後的股票"
    },
    "select_industry": {
        "en": "Select Industry",
        "zh": "選擇行業"
    },
    "sort_by": {
        "en": "Sort By",
        "zh": "排序依據"
    },
    "reset_filter": {
        "en": "Reset Filter",
        "zh": "重置篩選"
    },
    "analyze_stock": {
        "en": "Analyze",
        "zh": "分析"
    },
    "analyzing_stocks": {
        "en": "Analyzing stocks...",
        "zh": "正在分析股票..."
    },
    "no_stock_data": {
        "en": "No stock data available",
        "zh": "無股票數據可用"
    },
    "no_matching_criteria": {
        "en": "No stocks match your criteria",
        "zh": "沒有股票符合您的條件"
    },
    "no_valid_price_data": {
        "en": "No stocks with valid price data found in this selection. Try selecting a different industry.",
        "zh": "此選擇中未找到有效價格數據的股票。請嘗試選擇不同的行業。"
    },
    "no_price_data_available": {
        "en": "No price data available for this stock",
        "zh": "此股票無價格數據可用"
    },
    "select_stock_to_analyze": {
        "en": "Select a stock to analyze",
        "zh": "選擇要分析的股票"
    },
    "choose_stock_message": {
        "en": "Choose a stock from the filtered list to see detailed analysis, charts, and AI insights.",
        "zh": "從篩選列表中選擇股票以查看詳細分析、圖表和AI見解。"
    },
    "ai_analyzing": {
        "en": "AI is analyzing...",
        "zh": "AI正在分析..."
    },
    "volume_label": {
        "en": "Volume:",
        "zh": "成交量："
    },
    "rsi_label": {
        "en": "RSI",
        "zh": "RSI"
    },
    "sma_5_label": {
        "en": "SMA 5",
        "zh": "5日均線"
    },
    "sma_10_label": {
        "en": "SMA 10",
        "zh": "10日均線"
    },
    "finmind_api_remaining": {
        "en": "FinMind API Usage Remaining:",
        "zh": "FinMind API剩餘使用量："
    },
    
    # Sort options
    "sort_stock_id": {
        "en": "Stock ID",
        "zh": "股票代碼"
    },
    "sort_company_name": {
        "en": "Company Name",
        "zh": "公司名稱"
    },
    "sort_price": {
        "en": "Price",
        "zh": "價格"
    },
    "sort_price_change": {
        "en": "Price Change %",
        "zh": "價格變動%"
    },
    
    # Page names for navigation
    "dashboard": {
        "en": "Dashboard",
        "zh": "儀表板"
    },
    "stock_investments": {
        "en": "Stock Investments",
        "zh": "股票投資"
    },
    "documentation": {
        "en": "Documentation",
        "zh": "說明文件"
    },
    
    # AI Stock Agent translations
    "financial_chatbot": {
        "en": "💬 Financial Chatbot",
        "zh": "💬 金融聊天機器人"
    },
    "best_stock_details": {
        "en": "📊 Best Stock Details",
        "zh": "📊 最佳股票詳情"
    },
    "clear_chat_history": {
        "en": "🧹 Clear Chat History",
        "zh": "🧹 清除聊天記錄"
    },
    "example_prompts": {
        "en": "Example Prompts:",
        "zh": "示例提示："
    },
    "best_stock_in": {
        "en": "Best stock in",
        "zh": "最佳股票在"
    },
    "ask_question_placeholder": {
        "en": "Ask a question (e.g., 'Best stock in 半導體業'):",
        "zh": "提出問題（例如：'半導體業最佳股票'）："
    },
    "generating_response": {
        "en": "Generating Response...",
        "zh": "生成回應中..."
    },
    "you": {
        "en": "🟢 You:",
        "zh": "🟢 您："
    },
    "agent": {
        "en": "🤖 Agent:",
        "zh": "🤖 機器人："
    },
    "close": {
        "en": "Close",
        "zh": "收盤"
    },
    "high": {
        "en": "High",
        "zh": "最高"
    },
    "low": {
        "en": "Low",
        "zh": "最低"
    },
    "price_chart_30_days": {
        "en": "📈 30-Day Price Chart",
        "zh": "📈 30日價格圖表"
    },
    "date": {
        "en": "Date",
        "zh": "日期"
    },
    "price_twd": {
        "en": "Price (TWD)",
        "zh": "價格（新台幣）"
    },
    "price": {
        "en": "Price",
        "zh": "價格"
    },
    "price_data_unavailable": {
        "en": "⚠️ Price data unavailable (API quota exhausted). Showing company information only.",
        "zh": "⚠️ 價格資料無法取得（API配額已用盡）。僅顯示公司資訊。"
    },
    "company_overview": {
        "en": "🧠 Company Overview",
        "zh": "🧠 公司概覽"
    },
    "company": {
        "en": "Company:",
        "zh": "公司："
    },
    "stock_id": {
        "en": "Stock ID:",
        "zh": "股票代碼："
    },
    "industry": {
        "en": "Industry:",
        "zh": "行業："
    },
    "generating_company_description": {
        "en": "Generating company description...",
        "zh": "生成公司描述中..."
    },
    "company_background": {
        "en": "Company Background:",
        "zh": "公司背景："
    },
    "ask_about_best_stock": {
        "en": "💡 Ask about the best stock in an industry to see details here.",
        "zh": "💡 詢問某行業的最佳股票以在此處查看詳情。"
    },
    "finmind_api_exhausted": {
        "en": "🚫 FinMind API Exhausted",
        "zh": "🚫 FinMind API已用盡"
    },
    "low_api_quota": {
        "en": "⚠️ Low API Quota",
        "zh": "⚠️ API配額不足"
    },
    "finmind_api": {
        "en": "✅ FinMind API",
        "zh": "✅ FinMind API"
    },
    "calls_remaining": {
        "en": "calls remaining",
        "zh": "次調用剩餘"
    },
    "resets_in": {
        "en": "Resets in",
        "zh": "重置於"
    },
    "minutes": {
        "en": "minutes",
        "zh": "分鐘"
    }
}

def get_current_language():
    """Get current language from session state, default to English"""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    return st.session_state.language

def set_language(lang_code):
    """Set language in session state"""
    st.session_state.language = lang_code

def get_text(key, lang=None):
    """Get translated text for current language"""
    if lang is None:
        lang = get_current_language()
    
    if key in TRANSLATIONS and lang in TRANSLATIONS[key]:
        return TRANSLATIONS[key][lang]
    else:
        # Fallback to English if translation not found
        return TRANSLATIONS.get(key, {}).get("en", key)

def is_all_value(value):
    """Check if a value represents 'All' in any language"""
    all_values = [get_text('all', 'en'), get_text('all', 'zh'), 'All', '全部']
    return value in all_values

def create_language_selector():
    """Create language selector widget"""
    current_lang = get_current_language()
    
    # Create a more visible language selector at the top
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        st.markdown("**Language / 語言**")
        
        # Simple text-only language selector
        lang_codes = list(LANGUAGES.keys())
        lang_options = [LANGUAGES[code]['name'] for code in lang_codes]
        current_index = lang_codes.index(current_lang)
        
        selected = st.radio(
            "",
            lang_options,
            index=current_index,
            key="language_selector",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Update language if changed
        selected_code = lang_codes[lang_options.index(selected)]
        if selected_code != current_lang:
            set_language(selected_code)
            st.rerun()
    
    st.markdown("---")
    return current_lang

def create_sidebar_navigation(current_page="dashboard"):
    """Create sidebar navigation for quick access to main features"""
    
    # Add CSS for consistent button styling and active state highlighting
    st.markdown("""
    <style>
    /* Active button highlighting for Quick Actions */
    .sidebar-btn-active {
        background-color: #1f77b4 !important;
        background: #1f77b4 !important;
        color: white !important;
        border: 1px solid #1f77b4 !important;
    }
    
    .sidebar-btn-active:hover {
        background-color: #1a6aa3 !important;
        background: #1a6aa3 !important;
        color: white !important;
    }
    
    /* Universal button reset for sidebar - override ALL possible selectors */
    [data-testid="stSidebar"] button,
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] div[data-testid="stButton"] button,
    [data-testid="stSidebar"] [role="button"],
    .sidebar-content button,
    .css-1d391kg button,
    .css-1d391kg .stButton > button,
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] .stButton > button {
        background-color: white !important;
        background: white !important;
        color: rgb(38, 39, 48) !important;
        border: 1px solid #cccccc !important;
        box-shadow: none !important;
        transition: none !important;
        outline: none !important;
    }
    
    /* All pseudo-states */
    [data-testid="stSidebar"] button:hover,
    [data-testid="stSidebar"] button:focus,
    [data-testid="stSidebar"] button:active,
    [data-testid="stSidebar"] button:visited,
    [data-testid="stSidebar"] .stButton > button:hover,
    [data-testid="stSidebar"] .stButton > button:focus,
    [data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] .stButton > button:visited,
    section[data-testid="stSidebar"] button:hover,
    section[data-testid="stSidebar"] button:focus,
    section[data-testid="stSidebar"] button:active,
    section[data-testid="stSidebar"] button:visited,
    section[data-testid="stSidebar"] .stButton > button:hover,
    section[data-testid="stSidebar"] .stButton > button:focus,
    section[data-testid="stSidebar"] .stButton > button:active,
    section[data-testid="stSidebar"] .stButton > button:visited {
        background-color: rgb(240, 242, 246) !important;
        background: rgb(240, 242, 246) !important;
        color: rgb(38, 39, 48) !important;
        border: 1px solid #cccccc !important;
        box-shadow: none !important;
        outline: none !important;
        transform: none !important;
    }
    
    /* Override secondary button types only - let primary buttons keep blue color */
    [data-testid="stSidebar"] button[kind="secondary"],
    [data-testid="stSidebar"] .stButton > button[kind="secondary"],
    section[data-testid="stSidebar"] button[kind="secondary"] {
        background-color: white !important;
        background: white !important;
        color: rgb(38, 39, 48) !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Ensure primary buttons show blue in sidebar */
    [data-testid="stSidebar"] button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] button[kind="primary"] {
        background-color: #1f77b4 !important;
        background: #1f77b4 !important;
        color: white !important;
        border: 1px solid #1f77b4 !important;
    }
    
    
    /* Specific overrides for known problematic selectors */
    [data-testid="stSidebar"] button[style*="rgb(255, 75, 75)"],
    [data-testid="stSidebar"] button[style*="rgb(19, 23, 32)"],
    [data-testid="stSidebar"] button[style*="blue"],
    [data-testid="stSidebar"] button[style*="#1f77b4"],
    [data-testid="stSidebar"] button[style*="#ff4b4b"],
    [data-testid="stSidebar"] button[class*="selected"],
    [data-testid="stSidebar"] button[class*="active"],
    [data-testid="stSidebar"] button[aria-pressed="true"] {
        background-color: white !important;
        background: white !important;
        color: rgb(38, 39, 48) !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Force reset after any state changes */
    [data-testid="stSidebar"] .stButton:after,
    [data-testid="stSidebar"] button:after {
        background-color: white !important;
        color: rgb(38, 39, 48) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Initialize language if not set
        if "language" not in st.session_state:
            st.session_state.language = "en"
            
        
        # Language selector at the top - always bilingual
        st.markdown("### Language / 語言")
        
        # Dropdown/selectbox language selector for sidebar
        lang_codes = list(LANGUAGES.keys())
        lang_options = [LANGUAGES[code]['name'] for code in lang_codes]
        current_lang = get_current_language()
        current_index = lang_codes.index(current_lang)
        
        selected_lang = st.selectbox(
            "",
            lang_options,
            index=current_index,
            key="sidebar_language_selector",
            label_visibility="collapsed"
        )
        
        # Update language if changed
        selected_code = lang_codes[lang_options.index(selected_lang)]
        if selected_code != current_lang:
            set_language(selected_code)
            st.rerun()
        
        st.markdown("---")
        
        st.markdown(f"## {get_text('navigation')}")
        
        # Quick Actions
        st.markdown(f"### {get_text('quick_actions')}")
        
        # Get current active tab/page
        current_tab = st.session_state.get('current_tab_key', '')
        
        # Create buttons with conditional styling
        stock_filter_button_type = "primary" if current_tab == "stock_filter" else "secondary"
        ai_agent_button_type = "primary" if current_tab == "ai_stock_agent" else "secondary"
        
        # Industry Analysis - highlight if active (any industry tab)
        is_industry_active = current_tab in ["food_industry", "home_living", "semiconductor", "ecommerce", 
                                           "agri_tech", "glass_ceramics", "cement", "paper", "sports_leisure", 
                                           "rubber", "oil_gas", "green_energy", "plastics", "shipping", 
                                           "cultural_creative", "agri_tech_business", "tourism", "trading_retail", 
                                           "optoelectronics", "biotechnology_medical"]
        industry_button_type = "primary" if is_industry_active else "secondary"
        
        # Stock Filter
        if st.button(get_text('stock_filter'), key="nav_stock_filter", use_container_width=True, type=stock_filter_button_type):
            st.session_state.current_tab_key = "stock_filter"
            st.switch_page("pages/1_Stock_Investments_股票投資.py")
        
        # AI Stock Agent  
        if st.button(get_text('ai_stock_agent'), key="nav_ai_agent", use_container_width=True, type=ai_agent_button_type):
            st.session_state.current_tab_key = "ai_stock_agent"
            st.switch_page("pages/1_Stock_Investments_股票投資.py")
        
        # Industry Analysis
        if st.button(get_text('industry_analysis'), key="nav_industries", use_container_width=True, type=industry_button_type):
            st.session_state.current_tab_key = "food_industry"
            st.switch_page("pages/1_Stock_Investments_股票投資.py")
        
        
