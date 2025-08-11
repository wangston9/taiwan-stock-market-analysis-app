# pages/1_Stock_Investments.py

import streamlit as st
from language_config import get_text, create_language_selector, create_sidebar_navigation

# Set page config with default title (will be overridden by sidebar)
st.set_page_config(page_title="Stock Investments", layout="wide")

# Add sidebar navigation for easy access
create_sidebar_navigation("stock_investments")

# Initialize session state for tab selection with persistence across language changes
if "stock_investments_tab" not in st.session_state:
    st.session_state.stock_investments_tab = 0

# Store the tab selection in a way that persists across language changes
if "current_tab_key" not in st.session_state:
    st.session_state.current_tab_key = "food_industry"

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem !important;
    }
    .stNumberInput {
        margin-bottom: -10px !important;
    }
    .stSlider {
        margin-top: -20px !important;
        margin-bottom: -10px !important;
    }
    .stMarkdown {
        margin-bottom: -10px !important;
    }
    .stTabs [role="tab"] {
        color: white !important;
        font-weight: 600;
        font-size: 15px;
    }
    
    /* Industry tab selector styling - MAIN CONTENT ONLY (exclude sidebar) */
    .main .stRadio > div[role="radiogroup"] > label:hover {
        background-color: #FFEB3B !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        color: #000000 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    
    /* Style the radio button container - MAIN CONTENT ONLY */
    .main .stRadio > div[role="radiogroup"] {
        display: flex !important;
        gap: 8px !important;
        background-color: #f0f2f6 !important;
        padding: 8px !important;
        border-radius: 10px !important;
    }
    
    /* Style individual radio labels - MAIN CONTENT ONLY */
    .main .stRadio > div[role="radiogroup"] > label {
        flex: 1 !important;
        text-align: center !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        background-color: white !important;
        border: 1px solid #ddd !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    /* Selected radio button style - yellow background - MAIN CONTENT ONLY */
    .main .stRadio > div[role="radiogroup"] > label:has(input:checked) {
        background-color: #FFD54F !important;
        color: #000000 !important;
        border-color: #FFC107 !important;
        font-weight: 600 !important;
    }
    
    /* Hide the actual radio circles - MAIN CONTENT ONLY */
    .main .stRadio input[type="radio"] {
        display: none !important;
    }
    
    /* Make labels look like buttons - MAIN CONTENT ONLY */
    .main .stRadio label {
        display: inline-block !important;
        user-select: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Define tab information - removed stock_filter and ai_stock_agent since they're in sidebar Quick Actions
tab_info = [
    ("food_industry", get_text('food_industry'), "modules/3_食品工業_Financial.py"),
    ("home_living", get_text('home_living'), "modules/4_居家生活_Financial.py"),
    ("semiconductor", get_text('semiconductor'), "modules/5_半導體業_Financial.py"),
    ("ecommerce", get_text('ecommerce'), "modules/6_電子商務業_Financial.py"),
    ("agri_tech", get_text('agri_tech'), "modules/7_農業科技_Financial.py"),
    ("glass_ceramics", get_text('glass_ceramics'), "modules/8_玻璃陶瓷_Financial.py"),
    ("cement", get_text('cement'), "modules/9_水泥工業_Financial.py"),
    ("paper", get_text('paper'), "modules/10_造紙工業_Financial.py"),
    ("sports_leisure", get_text('sports_leisure'), "modules/11_運動休閒類_Financial.py"),
    ("rubber", get_text('rubber'), "modules/12_橡膠工業_Financial.py"),
    ("oil_gas", get_text('oil_gas'), "modules/13_油電燃氣業_Financial.py"),
    ("green_energy", get_text('green_energy'), "modules/14_綠能環保類_Financial.py"),
    ("plastics", get_text('plastics'), "modules/15_塑膠工業_Financial.py"),
    ("shipping", get_text('shipping'), "modules/16_航運業_Financial.py"),
    ("cultural_creative", get_text('cultural_creative'), "modules/17_文化創意業_Financial.py"),
    ("agri_tech_business", get_text('agri_tech_business'), "modules/18_農業科技業_Financial.py"),
    ("tourism", get_text('tourism'), "modules/19_觀光事業_Financial.py"),
    ("trading_retail", get_text('trading_retail'), "modules/20_貿易百貨_Financial.py"),
    ("optoelectronics", get_text('optoelectronics'), "modules/21_光電業_Financial.py"),
    ("biotechnology_medical", get_text('biotechnology_medical'), "modules/22_生技醫療業_Financial.py")
]

# Handle removed tabs - if user clicks stock_filter or ai_stock_agent from sidebar, 
# show the appropriate module directly instead of trying to find it in tabs
if st.session_state.current_tab_key == "stock_filter":
    st.markdown(f"### {get_text('stock_filter')}")
    st.markdown("---")
    exec(open("modules/1_Stock_Filter_Enhanced.py").read())
    st.stop()
elif st.session_state.current_tab_key == "ai_stock_agent":
    st.markdown(f"### {get_text('ai_stock_agent')}")
    st.markdown("---")
    exec(open("modules/2_Stock_Agent.py").read())
    st.stop()

# Create manual tab system with session state preservation
tab_names = [info[1] for info in tab_info]

# Find current tab index based on stored key
current_tab_index = 0
for i, (tab_id, tab_name, module_path) in enumerate(tab_info):
    if tab_id == st.session_state.current_tab_key:
        current_tab_index = i
        break

# Ensure tab index is valid - if current key not found in industry tabs, default to first industry
if current_tab_index >= len(tab_info) or current_tab_index == 0 and st.session_state.current_tab_key not in [info[0] for info in tab_info]:
    current_tab_index = 0
    st.session_state.current_tab_key = tab_info[0][0]

# Create tab selector using radio buttons for better state control
st.markdown(f"### {get_text('industries_section')}")

selected_tab_name = st.radio(
    "",  # Empty label instead of 'select_industry'
    tab_names,
    index=current_tab_index,
    horizontal=True,
    key="tab_selector",
    label_visibility="collapsed"
)

# Update session state based on selection
selected_tab_index = tab_names.index(selected_tab_name)
selected_tab_id = tab_info[selected_tab_index][0]

if selected_tab_id != st.session_state.current_tab_key:
    st.session_state.current_tab_key = selected_tab_id
    st.session_state.stock_investments_tab = selected_tab_index

# Execute the selected module
selected_module_path = tab_info[selected_tab_index][2]
try:
    st.markdown("---")
    exec(open(selected_module_path).read())
except Exception as e:
    st.error(f"{get_text('error_loading_module')} {selected_tab_name}: {str(e)}")

# Custom CSS for better radio button styling to look like tabs - MAIN CONTENT ONLY
st.markdown("""
<style>
/* Fix radio button styling - MAIN CONTENT ONLY */
.main .stRadio > div {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.main .stRadio > div > label {
    background-color: #f0f2f6 !important;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 0.25rem;
    font-weight: 500;
}

.main .stRadio > div > label:hover {
    background-color: #e6e9ef !important;
    transform: translateY(-1px);
}

.main .stRadio > div > label[data-checked="true"] {
    background-color: #667eea !important;
    border-color: #667eea;
    font-weight: 600;
}

/* Fix text colors inside radio buttons - MAIN CONTENT ONLY */
.main .stRadio > div > label > div {
    color: #2c3e50 !important;
}

.main .stRadio > div > label:hover > div {
    color: #1a202c !important;
}

.main .stRadio > div > label[data-checked="true"] > div {
    color: white !important;
}

/* Hide radio button circles - MAIN CONTENT ONLY */
.main .stRadio > div > label > div:first-child {
    display: none;
}

/* Additional text color fixes - MAIN CONTENT ONLY */
.main .stRadio label p {
    color: #2c3e50 !important;
}

.main .stRadio label[data-checked="true"] p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

