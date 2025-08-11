# pages/2_Documentation_說明文件.py

import streamlit as st
import os
import glob
from datetime import datetime
from language_config import get_text, get_current_language, create_sidebar_navigation

def get_latest_data_update():
    """Get the latest modification date from data files"""
    try:
        # Get all data files
        data_files = []
        
        # Check finmind_data files
        finmind_files = glob.glob("finmind_data/*.csv")
        data_files.extend(finmind_files)
        
        # Check bank_data files
        if os.path.exists("bank_data/bank_gold_price.csv"):
            data_files.append("bank_data/bank_gold_price.csv")
        
        if not data_files:
            return datetime.now().strftime("%Y年%m月"), datetime.now().strftime("%B %Y")
        
        # Get the latest modification date
        latest_date = max(os.path.getmtime(file) for file in data_files)
        latest_datetime = datetime.fromtimestamp(latest_date)
        
        # Format for Chinese and English
        zh_format = latest_datetime.strftime("%Y年%m月")
        en_format = latest_datetime.strftime("%B %Y")
        
        return zh_format, en_format
    except Exception:
        # Fallback to current date if there's an error
        now = datetime.now()
        return now.strftime("%Y年%m月"), now.strftime("%B %Y")

# Page configuration
st.set_page_config(
    page_title="Documentation 說明文件",
    page_icon="📚",
    layout="wide"
)

# Add sidebar navigation
create_sidebar_navigation()

# Get current language
current_lang = get_current_language()

# Get latest data update dates
zh_update_date, en_update_date = get_latest_data_update()

# Main title
if current_lang == "zh":
    st.title("📚 應用程式說明文件")
    st.markdown("### 瞭解此財務分析平台的運作原理")
else:
    st.title("📚 Application Documentation")
    st.markdown("### Understanding How This Financial Analysis Platform Works")

# Create tabs for different sections
if current_lang == "zh":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 概述", 
        "📊 財務分析邏輯", 
        "🤖 AI整合", 
        "💾 資料來源與限制",
        "🚀 技術架構"
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Overview", 
        "📊 Financial Analysis Logic", 
        "🤖 AI Integration", 
        "💾 Data Sources & Limitations",
        "🚀 Technical Architecture"
    ])

# Tab 1: Overview
with tab1:
    if current_lang == "zh":
        st.markdown("""
        ## 應用程式概述
        
        這是一個專為台灣股市設計的智能財務分析平台，結合了傳統的價值投資理論與現代AI技術。
        
        ### 主要功能：
        
        1. **行業分析** 📈
           - 使用巴菲特價值投資原則評估16個主要產業
           - 自動計算財務健康分數
           - 視覺化呈現關鍵財務指標
        
        2. **股票篩選器** 🔍
           - 按產業篩選股票
           - 即時價格資料與技術指標
           - AI驅動的公司描述生成
        
        3. **AI股票助手** 🤖
           - 基於財務數據的智能推薦
           - 自然語言互動介面
           - 整合GPT-3.5進行深度分析
        
        ### 目標使用者：
        - 個人投資者尋求數據驅動的投資決策
        - 財務分析師需要快速產業概覽
        - 對台股有興趣的研究人員
        """)
    else:
        st.markdown("""
        ## Application Overview
        
        This is an intelligent financial analysis platform designed specifically for the Taiwan stock market, 
        combining traditional value investing principles with modern AI technology.
        
        ### Key Features:
        
        1. **Industry Analysis** 📈
           - Evaluates 16 major industries using Buffett's value investing principles
           - Automatically calculates financial health scores
           - Visualizes key financial metrics
        
        2. **Stock Filter** 🔍
           - Filter stocks by industry
           - Real-time price data and technical indicators
           - AI-powered company description generation
        
        3. **AI Stock Agent** 🤖
           - Intelligent recommendations based on financial data
           - Natural language interaction interface
           - Integrated GPT-3.5 for deep analysis
        
        ### Target Users:
        - Individual investors seeking data-driven investment decisions
        - Financial analysts needing quick industry overviews
        - Researchers interested in Taiwan's stock market
        """)

# Tab 2: Financial Analysis Logic
with tab2:
    if current_lang == "zh":
        st.markdown("""
        ## 財務分析邏輯
        
        ### 1. 巴菲特資產負債表規則 📊
        
        **通過條件：**
        - ✅ 現金 > 總債務
        - ✅ 負債權益比 < 0.8
        - ✅ 保留盈餘年增長率 > 0
        
        **評分邏輯：**
        ```python
        淨資產分數 = 現金 + 保留盈餘 - 總債務
        ```
        
        ### 2. 巴菲特損益表規則 📋
        
        **通過條件：**
        - ✅ 毛利率 > 30%
        - ✅ 利息毛利率 < 25%
        - ✅ 淨利率 > 5%
        - ✅ 每股盈餘成長且 > 0
        
        **評分邏輯：**
        ```python
        獲利能力分數 = 平均淨利潤（近期季度）
        ```
        
        ### 3. 費羅迪現金流規則 💰
        
        **通過條件：**
        - ✅ 營運現金流 > 0
        - ✅ 自由現金流 > 0
        - ✅ 淨債務變化 ≤ 0
        - ✅ 資本支出 < 營運現金流
        
        **評分邏輯：**
        ```python
        現金流分數 = 營運現金流 - 資本支出
        ```
        
        ### 排名系統
        
        每個類別（資產負債表、損益表、現金流）的前5名股票會根據以下因素選出：
        1. 通過百分比（符合所有條件的季度百分比）
        2. 絕對財務數值（如淨資產、淨利潤）
        3. 關鍵比率（如ROE、ROA）
        """)
    else:
        st.markdown("""
        ## Financial Analysis Logic
        
        ### 1. Buffett Balance Sheet Rules 📊
        
        **Pass Criteria:**
        - ✅ Cash > Total Debt
        - ✅ Debt-to-Equity < 0.8
        - ✅ Retained Earnings YoY Growth > 0
        
        **Scoring Logic:**
        ```python
        Net Worth Score = Cash + Retained Earnings - Total Debt
        ```
        
        ### 2. Buffett Income Statement Rules 📋
        
        **Pass Criteria:**
        - ✅ Gross Margin > 30%
        - ✅ Interest Margin < 25%
        - ✅ Net Profit Margin > 5%
        - ✅ EPS Growth and > 0
        
        **Scoring Logic:**
        ```python
        Profitability Score = Average Net Income (Recent Quarters)
        ```
        
        ### 3. Feroldi Cash Flow Rules 💰
        
        **Pass Criteria:**
        - ✅ Operating Cash Flow > 0
        - ✅ Free Cash Flow > 0
        - ✅ Net Debt Change ≤ 0
        - ✅ CapEx < Operating Cash Flow
        
        **Scoring Logic:**
        ```python
        Cash Flow Score = Operating Cash Flow - Capital Expenditure
        ```
        
        ### Ranking System
        
        Top 5 stocks in each category (Balance Sheet, Income Statement, Cash Flow) are selected based on:
        1. Pass Percentage (% of quarters meeting all criteria)
        2. Absolute Financial Values (e.g., Net Worth, Net Income)
        3. Key Ratios (e.g., ROE, ROA)
        """)

# Tab 3: AI Integration
with tab3:
    if current_lang == "zh":
        st.markdown("""
        ## AI整合架構
        
        ### 1. GPT-3.5 整合 🧠
        
        **用途：**
        - 生成公司業務描述
        - 分析財務數據並提供投資建議
        - 自然語言查詢處理
        
        **資料流程：**
        ```
        使用者查詢 → 資料擷取 → 格式化為表格 → GPT分析 → 結構化回應
        ```
        
        ### 2. LangChain Agent 架構 🔗
        
        **工具鏈：**
        - `get_best_stock_for_industry`: 擷取產業排名資料
        - `ConversationBufferMemory`: 維護對話上下文
        - `create_openai_functions_agent`: 函數調用能力
        
        **提示工程：**
        - 系統提示包含財務分析指導原則
        - 雙語支援（中文/英文）
        - 結構化輸出格式要求
        
        ### 3. 資料餵送策略 📊
        
        **提供給AI的資料：**
        ```python
        {
            "資產負債表前5名": [股票排名與指標],
            "損益表前5名": [股票排名與指標],
            "現金流前5名": [股票排名與指標],
            "平均通過率": 各類別百分比
        }
        ```
        
        **AI不接收的資料：**
        - 原始財務報表
        - 即時股價（除非特別請求）
        - 歷史價格走勢
        
        ### 4. 回應解析 🎯
        
        **正則表達式模式：**
        - 英文: `best stock|recommend|conclusion`
        - 中文: `基於分析|最佳股票是|結論`
        - 自動擷取股票代號與名稱
        """)
    else:
        st.markdown("""
        ## AI Integration Architecture
        
        ### 1. GPT-3.5 Integration 🧠
        
        **Use Cases:**
        - Generate company business descriptions
        - Analyze financial data and provide investment recommendations
        - Natural language query processing
        
        **Data Flow:**
        ```
        User Query → Data Retrieval → Format as Tables → GPT Analysis → Structured Response
        ```
        
        ### 2. LangChain Agent Architecture 🔗
        
        **Tool Chain:**
        - `get_best_stock_for_industry`: Retrieve industry ranking data
        - `ConversationBufferMemory`: Maintain conversation context
        - `create_openai_functions_agent`: Function calling capabilities
        
        **Prompt Engineering:**
        - System prompts contain financial analysis guidelines
        - Bilingual support (Chinese/English)
        - Structured output format requirements
        
        ### 3. Data Feeding Strategy 📊
        
        **Data Provided to AI:**
        ```python
        {
            "Balance Sheet Top 5": [Stock rankings & metrics],
            "Income Statement Top 5": [Stock rankings & metrics],
            "Cash Flow Top 5": [Stock rankings & metrics],
            "Average Pass Rates": Percentages by category
        }
        ```
        
        **Data NOT Sent to AI:**
        - Raw financial statements
        - Real-time stock prices (unless specifically requested)
        - Historical price trends
        
        ### 4. Response Parsing 🎯
        
        **Regex Patterns:**
        - English: `best stock|recommend|conclusion`
        - Chinese: `基於分析|最佳股票是|結論`
        - Automatic extraction of stock ID and name
        """)

# Tab 4: Data Sources & Limitations
with tab4:
    if current_lang == "zh":
        st.markdown("""
        ## 資料來源與限制
        
        ### 資料來源 📡
        
        **FinMind API**
        - 台灣股市財務數據
        - 每日價格資料
        - 產業分類資訊
        - 免費版本：600次調用/小時
        
        ### API限制與管理 ⚠️
        
        **目前限制：**
        - 每小時600次API調用
        - 每次調用可獲取一支股票的資料
        - 重置時間：每小時整點
        
        **優化策略：**
        1. **快取機制**
           ```python
           @st.cache_data(ttl=86400)  # 24小時快取
           def cached_stock_info():
               return get_taiwan_stock_info()
           ```
        
        2. **批次處理**
           - 產業資料預載入
           - 一次下載整個產業的財務數據
        
        3. **智能重試**
           - API配額耗盡時顯示警告
           - 自動計算重置時間
        
        ### 資料覆蓋範圍 📅
        
        - **財務報表**: 2020年至今（季度資料）
        - **股價資料**: 最近30天
        - **產業覆蓋**: 16個主要產業類別
        - **股票數量**: 約1,700支上市股票
        
        ### 已知限制 ⚠️
        
        1. **資料延遲**: 財務報表有1-2個月延遲
        2. **覆蓋不完整**: 某些小型股可能缺少資料
        3. **API配額**: 大量使用時可能耗盡
        4. **語言限制**: 財務數據欄位名稱為英文
        """)
    else:
        st.markdown("""
        ## Data Sources & Limitations
        
        ### Data Sources 📡
        
        **FinMind API**
        - Taiwan stock market financial data
        - Daily price data
        - Industry classification information
        - Free tier: 600 calls/hour
        
        ### API Limitations & Management ⚠️
        
        **Current Limits:**
        - 600 API calls per hour
        - Each call retrieves data for one stock
        - Reset time: Every hour on the hour
        
        **Optimization Strategies:**
        1. **Caching Mechanism**
           ```python
           @st.cache_data(ttl=86400)  # 24-hour cache
           def cached_stock_info():
               return get_taiwan_stock_info()
           ```
        
        2. **Batch Processing**
           - Pre-load industry data
           - Download entire industry financial data at once
        
        3. **Smart Retry**
           - Display warning when API quota exhausted
           - Auto-calculate reset time
        
        ### Data Coverage 📅
        
        - **Financial Statements**: 2020 to present (quarterly)
        - **Price Data**: Last 30 days
        - **Industry Coverage**: 16 major industry categories
        - **Stock Count**: ~1,700 listed stocks
        
        ### Known Limitations ⚠️
        
        1. **Data Lag**: Financial statements have 1-2 month delay
        2. **Incomplete Coverage**: Some small-cap stocks may lack data
        3. **API Quota**: May exhaust with heavy usage
        4. **Language Limitation**: Financial data column names in English
        """)

# Tab 5: Technical Architecture
with tab5:
    if current_lang == "zh":
        st.markdown("""
        ## 技術架構
        
        ### 技術堆疊 🔧
        
        **前端框架:**
        - Streamlit 1.29+
        - Plotly (互動式圖表)
        - HTML/CSS (自定義樣式)
        
        **後端處理:**
        - Python 3.8+
        - Pandas (資料處理)
        - NumPy (數值計算)
        
        **AI/ML整合:**
        - OpenAI GPT-3.5
        - LangChain (Agent框架)
        - Regular Expressions (模式匹配)
        
        ### 檔案結構 📁
        
        ```
        Personal_Finance_App/
        ├── pages/
        │   ├── 1_Stock_Investments_股票投資.py
        │   └── 2_Documentation_說明文件.py
        ├── modules/
        │   ├── 3_Stock_Filter.py
        │   ├── 3_Stock_Filter_Enhanced.py
        │   ├── 4_Stock_Agent.py
        │   └── [產業分析模組 x16]
        ├── finmind_data/
        │   └── [產業CSV檔案]
        ├── finmind_tools.py (核心功能)
        ├── language_config.py (多語言支援)
        └── Dashboard.py (主頁面)
        ```
        
        ### 關鍵功能模組 🔑
        
        **finmind_tools.py:**
        - `analyze_csv_to_wide_df()`: 資料透視處理
        - `run_buffett_analysis()`: 巴菲特規則計算
        - `preload_all_industry_rankings()`: 預載入排名
        - `get_best_stock_for_industry()`: AI工具函數
        
        **language_config.py:**
        - 雙語支援系統
        - 動態語言切換
        - UI元件翻譯
        
        ### 部署考量 🚀
        
        **推薦平台:**
        - Hugging Face Spaces (免費、穩定)
        - Streamlit Cloud (原生支援)
        
        **環境需求:**
        ```
        streamlit>=1.29.0
        pandas>=2.0.0
        plotly>=5.0.0
        openai>=1.0.0
        langchain>=0.1.0
        python-dotenv>=1.0.0
        ```
        
        ### 效能優化 ⚡
        
        1. **快取策略**: 使用`@st.cache_data`減少API調用
        2. **延遲載入**: 只在需要時載入產業資料
        3. **會話狀態**: 使用`st.session_state`保持資料
        4. **批次處理**: 合併多個API請求
        """)
    else:
        st.markdown("""
        ## Technical Architecture
        
        ### Technology Stack 🔧
        
        **Frontend Framework:**
        - Streamlit 1.29+
        - Plotly (interactive charts)
        - HTML/CSS (custom styling)
        
        **Backend Processing:**
        - Python 3.8+
        - Pandas (data processing)
        - NumPy (numerical computation)
        
        **AI/ML Integration:**
        - OpenAI GPT-3.5
        - LangChain (Agent framework)
        - Regular Expressions (pattern matching)
        
        ### File Structure 📁
        
        ```
        Personal_Finance_App/
        ├── pages/
        │   ├── 1_Stock_Investments_股票投資.py
        │   └── 2_Documentation_說明文件.py
        ├── modules/
        │   ├── 3_Stock_Filter.py
        │   ├── 3_Stock_Filter_Enhanced.py
        │   ├── 4_Stock_Agent.py
        │   └── [Industry Analysis Modules x16]
        ├── finmind_data/
        │   └── [Industry CSV Files]
        ├── finmind_tools.py (Core Functions)
        ├── language_config.py (Multi-language Support)
        └── Dashboard.py (Main Page)
        ```
        
        ### Key Function Modules 🔑
        
        **finmind_tools.py:**
        - `analyze_csv_to_wide_df()`: Data pivot processing
        - `run_buffett_analysis()`: Buffett rules calculation
        - `preload_all_industry_rankings()`: Pre-load rankings
        - `get_best_stock_for_industry()`: AI tool function
        
        **language_config.py:**
        - Bilingual support system
        - Dynamic language switching
        - UI component translations
        
        ### Deployment Considerations 🚀
        
        **Recommended Platforms:**
        - Hugging Face Spaces (free, stable)
        - Streamlit Cloud (native support)
        
        **Environment Requirements:**
        ```
        streamlit>=1.29.0
        pandas>=2.0.0
        plotly>=5.0.0
        openai>=1.0.0
        langchain>=0.1.0
        python-dotenv>=1.0.0
        ```
        
        ### Performance Optimization ⚡
        
        1. **Caching Strategy**: Use `@st.cache_data` to reduce API calls
        2. **Lazy Loading**: Load industry data only when needed
        3. **Session State**: Use `st.session_state` to persist data
        4. **Batch Processing**: Combine multiple API requests
        """)

# Add footer
st.markdown("---")
if current_lang == "zh":
    st.info("💡 **提示**: 此文件會根據您選擇的語言自動切換內容。")
    st.caption(f"最後更新: {zh_update_date}")
else:
    st.info("💡 **Tip**: This documentation automatically switches content based on your selected language.")
    st.caption(f"Last Updated: {en_update_date}")