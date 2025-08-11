# pages/4_Stock_Agents.py

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from finmind_tools import get_best_stock_for_industry, get_taiwan_stock_info, get_price_30days, get_api_quota_info, preload_all_industry_rankings
import plotly.graph_objs as go
import re
from language_config import get_text, get_current_language

# --- Preload all industry rankings for the agent ---
if "industry_rankings_loaded" not in st.session_state:
    with st.spinner("Loading industry data for agent..."):
        preload_all_industry_rankings()
    st.session_state.industry_rankings_loaded = True

def clean_markdown_asterisks(text):
    """Remove markdown bold formatting asterisks from text"""
    if text is None:
        return ""
    # Remove ** bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove single * italic formatting if needed
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text

# --- Load API key ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("❌ OPENAI_API_KEY not found. Please check your .env file.")
    st.stop()

# --- Chatbot Setup ---
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",#"gpt-4o",
    temperature=0,
    api_key=openai_api_key,
    streaming=True
)
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

tools = [get_best_stock_for_industry]

prompt = ChatPromptTemplate.from_messages([
    ("system", 
"""
You are a helpful financial assistant capable of analyzing stock metrics, rankings, and industry performance.

You receive structured data for a given industry, including metrics like average ratios, margins, EPS, free cash flow, and a '% Passed' score for each category (balance sheet, income statement, cash flow).

📌 '% Passed' reflects the **percentage of quarters (2020 to present)** where a stock met **all defined conditions** for that category.

However, do **not focus solely on '% Passed'**. Use it as **one factor among many**. Your job is to analyze the stock **holistically** — balancing financial health (e.g. cash/debt, equity), profitability (e.g. margins, EPS), and cash flow strength.

Summarize strengths and weaknesses clearly for each category, and then give a reasoned conclusion about the best stock in the industry.

IMPORTANT: In your conclusion, clearly state which stock is the best choice using this format:
"Based on the analysis, [StockName] (StockID) is the best stock in this industry because..."
or "The best stock is [StockName] (StockID) due to..."

Always include both the stock name and its 4-digit ID in parentheses when stating your final recommendation.
"""
),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=False,
    return_intermediate_steps=False,
    return_direct=True
)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "best_stock_id" not in st.session_state:
    st.session_state.best_stock_id = None

if "best_stock_name" not in st.session_state:
    st.session_state.best_stock_name = None

if "page_initialized" not in st.session_state:
    st.session_state.page_initialized = False


# Enhanced CSS for better UX
st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 20px 20px 5px 20px;
}
.user-message * {
    color: white !important;
}
.agent-message {
    background: #f8f9fa !important;
    color: #333333 !important;
    border-left: 4px solid #4ECDC4;
    border-radius: 5px 20px 20px 20px;
}
.agent-message * {
    color: #333333 !important;
}
.prompt-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.5rem;
    margin: 1rem 0;
}
.prompt-button {
    background: linear-gradient(45deg, #FF9A8B, #A8E6CF);
    border: none;
    padding: 0.8rem;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
}
.prompt-button:hover {
    transform: translateY(-2px);
}

/* Fix Streamlit button styling issues - Better contrast */
div.stButton > button:first-child {
    background: linear-gradient(45deg, #4A90E2, #357ABD) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
}

div.stButton > button:first-child:hover {
    background: linear-gradient(45deg, #5BA0F2, #4080CD) !important;
    transform: translateY(-2px) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.4) !important;
}

div.stButton > button:first-child:active {
    background: linear-gradient(45deg, #3A80D2, #2A60AD) !important;
    color: white !important;
    transform: translateY(0px) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.4) !important;
}

div.stButton > button:first-child:focus {
    background: linear-gradient(45deg, #4A90E2, #357ABD) !important;
    color: white !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.3) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
}
.api-status {
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(10px);
    padding: 0.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)

# --- FinMind API Quota Status ---
quota_info = get_api_quota_info()
if quota_info:
    remaining = quota_info["remaining"]
    limit = quota_info["limit"]
    minutes_until_reset = quota_info["minutes_until_reset"]
    
    if quota_info["is_exhausted"]:
        st.markdown(f"""
        <div class="api-status" style="background: rgba(255, 107, 107, 0.1); border-left: 4px solid #FF6B6B;">
            {get_text('finmind_api_exhausted')}: {remaining}/{limit} {get_text('calls_remaining')}. {get_text('resets_in')} {minutes_until_reset} {get_text('minutes')}.
        </div>
        """, unsafe_allow_html=True)
    elif remaining < 50:
        st.markdown(f"""
        <div class="api-status" style="background: rgba(255, 193, 7, 0.1); border-left: 4px solid #FFC107;">
            {get_text('low_api_quota')}: {remaining}/{limit} {get_text('calls_remaining')}. {get_text('resets_in')} {minutes_until_reset} {get_text('minutes')}.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="api-status" style="background: rgba(78, 205, 196, 0.1); border-left: 4px solid #4ECDC4;">
            {get_text('finmind_api')}: {remaining}/{limit} {get_text('calls_remaining')}. {get_text('resets_in')} {minutes_until_reset} {get_text('minutes')}.
        </div>
        """, unsafe_allow_html=True)

# --- Header Row (2 columns) ---
header_col1, header_col2 = st.columns([1.0, 1.3])

with header_col1:
    st.markdown(f"""
        <div style='line-height:1.2; margin-top:0; margin-bottom:4px; font-size:20px; font-weight:600'>
            {get_text('financial_chatbot')}
        </div>
        <hr style='margin-top:2px; margin-bottom:6px; border: none; height: 1px; background: #AAA;'>
    """, unsafe_allow_html=True)

with header_col2:
    st.markdown(f"""
        <div style='line-height:1.2; margin-top:0; margin-bottom:4px; font-size:20px; font-weight:600'>
            {get_text('best_stock_details')}
        </div>
        <hr style='margin-top:2px; margin-bottom:6px; border: none; height: 1px; background: #AAA;'>
    """, unsafe_allow_html=True)

# --- Main Content ---
col1, col2 = st.columns([1.0, 1.3])

with col1:
    if st.button(get_text('clear_chat_history')):
        st.session_state.chat_history = []
        memory.chat_memory.messages = []
        st.session_state.user_input = ""

    # --- Clickable Prompt Buttons ---
    # Simple solution: Show prompts unless actively processing
    # On first page load, wait one cycle to avoid shadow
    show_prompts_now = True
    
    if st.session_state.user_input and not st.session_state.chat_history:
        # We're processing the first query - hide prompts
        show_prompts_now = False
    elif st.session_state.user_input and st.session_state.chat_history:
        # Processing subsequent query - check if it's in history yet
        last_query = st.session_state.chat_history[-1][0] if st.session_state.chat_history else ""
        if st.session_state.user_input != last_query:
            show_prompts_now = False
    
    if show_prompts_now:
        st.markdown(f"### {get_text('example_prompts')}")
        
        # Organize prompts in a grid for better display
        all_industries = [
            "食品工業", "居家生活", "半導體業", "電子商務業",
            "農業科技", "玻璃陶瓷", "水泥工業", "造紙工業", 
            "運動休閒類", "橡膠工業", "油電燃氣業", "綠能環保類", 
            "塑膠工業", "航運業", "文化創意業", "農業科技業", "觀光事業", "貿易百貨", "光電業", "生技醫療業"
        ]
        
        # Industry translation mapping for buttons
        industry_translation = {
            "食品工業": get_text('food_industry'),
            "居家生活": get_text('home_living'),
            "半導體業": get_text('semiconductor'),
            "電子商務業": get_text('ecommerce'),
            "農業科技": get_text('agri_tech'),
            "玻璃陶瓷": get_text('glass_ceramics'),
            "水泥工業": get_text('cement'),
            "造紙工業": get_text('paper'),
            "運動休閒類": get_text('sports_leisure'),
            "橡膠工業": get_text('rubber'),
            "油電燃氣業": get_text('oil_gas'),
            "綠能環保類": get_text('green_energy'),
            "塑膠工業": get_text('plastics'),
            "航運業": get_text('shipping'),
            "文化創意業": get_text('cultural_creative'),
            "農業科技業": get_text('agri_tech_business'),
            "觀光事業": get_text('tourism'),
            "貿易百貨": get_text('trading_retail'),
            "光電業": get_text('optoelectronics'),
            "生技醫療業": get_text('biotechnology_medical')
        }
        
        # Create rows for button layout (20 industries now)
        rows = [all_industries[i:i+5] for i in range(0, len(all_industries), 5)]
        
        for row in rows:
            cols = st.columns(len(row))
            for i, industry in enumerate(row):
                # Use translated industry name for display
                translated_industry = industry_translation.get(industry, industry)
                prompt_text = f"{get_text('best_stock_in')} {translated_industry}"
                if cols[i].button(prompt_text, key=f"btn_{industry}"):
                    # But keep the Chinese name for the prompt since AI agent logic expects Chinese names
                    chinese_prompt = f"{get_text('best_stock_in')} {industry}"
                    st.session_state.user_input = chinese_prompt

    # --- Main Input ---
    st.session_state.user_input = st.text_input(
        get_text('ask_question_placeholder'), 
        value=st.session_state.user_input, 
        key="text_input"
    )

    if st.session_state.user_input:
        # Show agent header first
        st.markdown(f"""
        <div class="chat-message agent-message">
            <strong>{get_text('agent')}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Extract industry name from user input
        user_query = st.session_state.user_input
        industry_name = ""
        
        # Try to extract industry from common patterns (Chinese and English)
        industry_patterns = {
            "食品工業": ["食品工業", "food industry", "food"],
            "居家生活": ["居家生活", "home", "living"],
            "半導體業": ["半導體業", "semiconductor"],
            "電子商務業": ["電子商務業", "ecommerce", "e-commerce"],
            "農業科技": ["農業科技", "agricultural technology", "agri tech"],
            "玻璃陶瓷": ["玻璃陶瓷", "glass", "ceramics"],
            "水泥工業": ["水泥工業", "cement"],
            "造紙工業": ["造紙工業", "paper"],
            "運動休閒類": ["運動休閒類", "sports", "leisure"],
            "橡膠工業": ["橡膠工業", "rubber"],
            "油電燃氣業": ["油電燃氣業", "oil", "gas", "utilities"],
            "綠能環保類": ["綠能環保類", "green energy", "environmental"],
            "塑膠工業": ["塑膠工業", "plastics"],
            "航運業": ["航運業", "shipping"],
            "文化創意業": ["文化創意業", "cultural", "creative"],
            "農業科技業": ["農業科技業", "agricultural technology business"],
            "觀光事業": ["觀光事業", "tourism", "travel", "hospitality", "hotel"],
            "貿易百貨": ["貿易百貨", "trading", "department stores", "retail", "convenience"],
            "光電業": ["光電業", "optoelectronics", "opto", "LED", "display", "optical", "photonics"],
            "生技醫療業": ["生技醫療業", "biotechnology", "biotech", "medical", "pharmaceutical", "pharma", "healthcare", "bio", "medicine"]
        }
        
        for industry_chinese, patterns in industry_patterns.items():
            for pattern in patterns:
                if pattern.lower() in user_query.lower():
                    industry_name = industry_chinese
                    break
            if industry_name:
                break
        
        # Get the tool result first (this provides the data to the LLM)
        if industry_name:
            tool_result = get_best_stock_for_industry(industry_name)
        else:
            tool_result = f"Could not identify specific industry from query: {user_query}"
        
        # Create language-aware system prompt
        current_lang = get_current_language()
        
        if current_lang == "zh":
            system_prompt = """你是一位專業的金融分析師，能夠分析股票指標、排名和行業表現。

你會收到特定行業的結構化數據，包括平均比率、利潤率、每股盈餘、自由現金流，以及各類別（資產負債表、損益表、現金流）的「通過百分比」。

📌「通過百分比」反映了從2020年至今，該股票在各季度中**符合所有定義條件**的百分比。

但是，**不要只關注「通過百分比」**。將其作為**眾多因素之一**。你的工作是**全面分析**股票——平衡財務健康（如現金/債務、股權）、盈利能力（如利潤率、每股盈餘）和現金流強度。

請按照以下結構提供詳細分析：

## 資產負債表分析
分析每隻股票的財務健康狀況，包括現金/債務比率、負債/權益比率、通過百分比等，並說明各股票的優勢和劣勢。

## 損益表分析  
評估每隻股票的盈利能力，包括毛利率、淨利率、每股盈餘、通過百分比等，並比較各股票的表現。

## 現金流分析
檢視每隻股票的現金流強度，包括自由現金流、經營現金流、通過百分比等，並評估其現金產生能力。

## 結論
綜合所有分析，明確說明哪隻股票是最佳選擇，使用以下格式：
"[股票名稱]（股票代號）是該行業最佳股票，因為..."
或"最佳股票是[股票名稱]（股票代號），原因是..."

重要格式要求：
1. 絶對不要使用「我認為」、「我覺得」、「我想」、「我相信」等主觀表達
2. 不要使用**粗體**格式
3. 直接陳述事實和結論
4. 在陳述最終推薦時，請務必同時包含股票名稱和4位數股票代號（括號內）

請提供詳細且結構化的分析。"""
        else:
            system_prompt = """You are a helpful financial assistant capable of analyzing stock metrics, rankings, and industry performance.

You receive structured data for a given industry, including metrics like average ratios, margins, EPS, free cash flow, and a '% Passed' score for each category (balance sheet, income statement, cash flow).

📌 '% Passed' reflects the **percentage of quarters (2020 to present)** where a stock met **all defined conditions** for that category.

However, do **not focus solely on '% Passed'**. Use it as **one factor among many**. Your job is to analyze the stock **holistically** — balancing financial health (e.g. cash/debt, equity), profitability (e.g. margins, EPS), and cash flow strength.

Summarize strengths and weaknesses clearly for each category, and then give a reasoned conclusion about the best stock in the industry.

IMPORTANT: In your conclusion, clearly state which stock is the best choice using this format:
"Based on the analysis, [StockName] (StockID) is the best stock in this industry because..."
or "The best stock is [StockName] (StockID) due to..."

Always include both the stock name and its 4-digit ID in parentheses when stating your final recommendation."""

        full_prompt = f"""{system_prompt}

User Question: {user_query}

Industry Analysis Data:
{tool_result}

Please provide your analysis and recommendation:"""
        
        # Stream the LLM response directly
        def generate_response():
            for chunk in llm.stream(full_prompt):
                yield chunk.content
        
        # Use Streamlit's write_stream for real streaming
        response = st.write_stream(generate_response)
        
        # Add to chat history and memory
        st.session_state.chat_history.append((st.session_state.user_input, response))
        memory.chat_memory.add_user_message(st.session_state.user_input)
        memory.chat_memory.add_ai_message(response)
        
        # Extract the best stock from response
        # Look for patterns like "best stock is", "recommend", "top pick", "#1", or conclusion section
        # Include both English and Chinese patterns
        best_stock_patterns = [
            # English patterns
            r'(?:best stock|top pick|recommend|#1|number one|winner)(?:\s+is)?[:\s]+([^\s]+)\s*\((\d{4})\)',
            r'(?:conclusion|overall|final recommendation)[:\s\S]*?([^\s]+)\s*\((\d{4})\)',
            r'(\w+)\s*\((\d{4})\)(?:\s+is|stands out as)?\s+(?:the best|top|recommended)',
            r'(?:I recommend|would recommend|choose)\s+([^\s]+)\s*\((\d{4})\)',
            r'([^\s]+)\s*\((\d{4})\)\s+(?:emerges|appears|seems)?\s*(?:as|to be)?\s*(?:the)?\s*(?:best|strongest|top)',
            # Chinese patterns
            r'(?:基於分析|最佳股票是|推薦|建議)[，,：:\s]*([^\s，,（\(]+)\s*[（\(](\d{4})[）\)]',
            r'(?:結論|總結|綜合)[：:\s\S]*?([^\s，,（\(]+)\s*[（\(](\d{4})[）\)]',
            r'([^\s，,（\(]+)\s*[（\(](\d{4})[）\)]\s*(?:是|為)?(?:該行業)?(?:最佳|最好|首選)',
            r'(?:我推薦|建議選擇|選擇)\s*([^\s，,（\(]+)\s*[（\(](\d{4})[）\)]'
        ]
        
        stock_found = False
        for pattern in best_stock_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                # Get the last match (likely in conclusion)
                stock_name, stock_id = matches[-1]
                # Clean the stock name of any subjective phrases and markdown
                stock_name = stock_name.replace("我認為", "").replace("我覺得", "").replace("我想", "").replace("我相信", "")
                stock_name = clean_markdown_asterisks(stock_name)
                stock_name = stock_name.strip()
                st.session_state.best_stock_id = stock_id
                st.session_state.best_stock_name = stock_name
                stock_found = True
                break
        
        # Fallback: look for any stock ID in conclusion section (both English and Chinese)
        if not stock_found:
            conclusion_match = re.search(r'(?:conclusion|overall|summary|結論|總結|綜合)[:\s\S]*', response, re.IGNORECASE)
            if conclusion_match:
                conclusion_text = conclusion_match.group()
                # Look for pattern: CompanyName (1234) in both English and Chinese contexts
                stock_matches = re.findall(r'([^\s，,（\(]+)\s*[（\(](\d{4})[）\)]', conclusion_text)
                if stock_matches:
                    stock_name, stock_id = stock_matches[0]  # Take first stock in conclusion
                    # Clean the stock name
                    stock_name = stock_name.replace("我認為", "").replace("我覺得", "").replace("我想", "").replace("我相信", "")
                    stock_name = clean_markdown_asterisks(stock_name)
                    stock_name = stock_name.strip()
                    st.session_state.best_stock_id = stock_id
                    st.session_state.best_stock_name = stock_name
                    stock_found = True
        
        # Last fallback: find the first mentioned stock with ID (handle both English and Chinese punctuation)
        if not stock_found:
            first_stock = re.search(r'([^\s，,（\(]+)\s*[（\(](\d{4})[）\)]', response)
            if first_stock:
                stock_name = first_stock.group(1)
                # Clean the stock name
                stock_name = stock_name.replace("我認為", "").replace("我覺得", "").replace("我想", "").replace("我相信", "")
                stock_name = clean_markdown_asterisks(stock_name)
                stock_name = stock_name.strip()
                st.session_state.best_stock_id = first_stock.group(2)
                st.session_state.best_stock_name = stock_name
        
        st.session_state.user_input = ""  # Clear after use

    # Show chat history (exclude the most recent entry which is already being streamed above)
    chat_to_display = st.session_state.chat_history[:-1] if st.session_state.chat_history else []
    
    for q, a in reversed(chat_to_display):
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>{get_text('you')}</strong> {q}
        </div>
        """, unsafe_allow_html=True)
        
        # Agent response - use a clean container approach
        st.markdown(f"""
        <div class="chat-message agent-message">
            <strong>{get_text('agent')}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Use a clean expander-like container for the response
        with st.container():
            st.markdown(a)

with col2:
    if st.session_state.best_stock_id:
        # Display stock info
        st.markdown(f"### 🏢 {clean_markdown_asterisks(st.session_state.best_stock_name)} ({st.session_state.best_stock_id})")
        
        # Get and display price data
        df_price = get_price_30days(st.session_state.best_stock_id)
        
        if not df_price.empty:
            # Latest price info
            latest_price = df_price.iloc[-1]
            prev_close = df_price.iloc[-2]['close'] if len(df_price) > 1 else latest_price['close']
            price_change = latest_price['close'] - prev_close
            price_change_pct = (price_change / prev_close) * 100 if prev_close != 0 else 0
            
            # Display metrics
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
            with col_metrics1:
                st.metric(get_text('close'), f"${latest_price['close']:.2f}", f"{price_change:.2f} ({price_change_pct:.2f}%)")
            with col_metrics2:
                st.metric(get_text('high'), f"${latest_price['max']:.2f}")
            with col_metrics3:
                st.metric(get_text('low'), f"${latest_price['min']:.2f}")
            
            # Candlestick chart
            st.markdown(f"#### {get_text('price_chart_30_days')}")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df_price["date"],
                open=df_price["open"],
                high=df_price["max"],
                low=df_price["min"],
                close=df_price["close"],
                name="Price"
            ))
            fig.update_layout(
                xaxis_title=get_text('date'),
                yaxis_title=get_text('price_twd'),
                height=350,
                xaxis_rangeslider_visible=False,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Show a warning about API limits but still show company info
            st.warning(get_text('price_data_unavailable'))
            
        # Always show Company Overview regardless of price data availability
        st.markdown(f"#### {get_text('company_overview')}")
        st.info(f"{get_text('company')} {clean_markdown_asterisks(st.session_state.best_stock_name)}")
        st.info(f"{get_text('stock_id')} {st.session_state.best_stock_id}")
        
        # Try to get industry from local database
        stock_info_df = get_taiwan_stock_info()
        industry = "N/A"
        if not stock_info_df.empty:
            company_row = stock_info_df[stock_info_df['stock_id'] == st.session_state.best_stock_id]
            if not company_row.empty:
                industry = company_row.iloc[0].get('industry_category', 'N/A')
        
        if industry != "N/A":
            st.info(f"{get_text('industry')} {industry}")
        
        # Always use OpenAI to generate company description
        try:
            current_lang = get_current_language()
            
            if current_lang == "zh":
                if industry != "N/A":
                    prompt = f"""
                    簡要描述{st.session_state.best_stock_name}（台股代號：{st.session_state.best_stock_id}）的業務內容。
                    該公司屬於{industry}行業。
                    請用2-3句話提供簡潔的公司背景和主要業務活動。
                    重點介紹公司主要業務、產品/服務和市場地位。
                    
                    重要規則：
                    1. 請直接陳述事實，絕對不要使用「我認為」、「我覺得」、「我想」、「我相信」等主觀表達
                    2. 直接以公司名稱開頭，例如：「{st.session_state.best_stock_name}是...」
                    3. 不要使用任何markdown格式（如**粗體**）
                    
                    請用繁體中文回答。
                    """
                else:
                    prompt = f"""
                    簡要描述{st.session_state.best_stock_name}（台股代號：{st.session_state.best_stock_id}）的業務內容。
                    這是一家台灣公司。請用2-3句話提供簡潔的公司背景和主要業務活動。
                    重點介紹公司主要業務、產品/服務和市場地位。
                    
                    重要規則：
                    1. 請直接陳述事實，絕對不要使用「我認為」、「我覺得」、「我想」、「我相信」等主觀表達
                    2. 直接以公司名稱開頭，例如：「{st.session_state.best_stock_name}是...」
                    3. 不要使用任何markdown格式（如**粗體**）
                    
                    請用繁體中文回答。
                    """
            else:
                if industry != "N/A":
                    prompt = f"""
                    Briefly describe what {st.session_state.best_stock_name} (Taiwan stock ID: {st.session_state.best_stock_id}) does.
                    The company is in the {industry} industry sector. 
                    Provide a concise company background and main business activities in 2-3 sentences.
                    Focus on what the company does, their main products/services, and market position.
                    """
                else:
                    prompt = f"""
                    Briefly describe what {st.session_state.best_stock_name} (Taiwan stock ID: {st.session_state.best_stock_id}) does.
                    This is a Taiwanese company. Provide a concise company background and main business activities in 2-3 sentences.
                    Focus on what the company does, their main products/services, and market position.
                    """
            
            with st.spinner(get_text('generating_company_description')):
                response = llm.invoke(prompt)
                st.markdown(f"##### {get_text('company_background')}")
                # Clean the response to remove unwanted phrases and markdown
                cleaned_response = response.content
                # Remove variations of "我認為" and similar subjective phrases
                cleaned_response = cleaned_response.replace("我認為", "")
                cleaned_response = cleaned_response.replace("我覺得", "")
                cleaned_response = cleaned_response.replace("我想", "")
                cleaned_response = cleaned_response.replace("我相信", "")
                # Also clean any markdown asterisks
                cleaned_response = clean_markdown_asterisks(cleaned_response)
                # Clean up any leading/trailing whitespace
                cleaned_response = cleaned_response.strip()
                st.markdown(cleaned_response)
                
        except Exception as e:
            st.markdown(f"##### {get_text('company_background')}")
            st.markdown(f"*{clean_markdown_asterisks(st.session_state.best_stock_name)} (ID: {st.session_state.best_stock_id}) was selected as the top performer based on comprehensive financial analysis across balance sheet strength, profitability metrics, and cash flow performance.*")
    else:
        st.info(get_text('ask_about_best_stock'))